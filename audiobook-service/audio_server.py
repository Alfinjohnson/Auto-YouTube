
import re
from time import sleep

from s3bucket import set_public_access
from const import DRAFT_TOPIC, S3_BUCKET
from flask import Flask, request, jsonify
import logging
from polly_main import polly, tts_task_resp, transcript_generator, get_word_by_transcript

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/test')
def hello_world():
    return 'Endpoint Responded Successfully'


@app.route('/createTopic', methods=['POST'])
def create_topic():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        logging.error("Title and description cannot be null or empty")
        return jsonify({"error": "Title and description cannot be null or empty"}), 400
    logging.info(f"Title: {title}, Description: {description}")
    # sending request to amazon polly
    audio_book_topic = re.sub(r'[^a-zA-Z0-9]', '', title)
    logging.info(f"audio_book_topic : {audio_book_topic}")
    logging.info(f"sending request to amazon polly ...")
    polly_response = polly(audio_book_topic, description, DRAFT_TOPIC)
    logging.info(f"amazon polly response : {polly_response}")
    logging.info(f"amazon polly  taskId : {polly_response['SynthesisTask']['TaskId']}")

    polly_file_name = polly_response['SynthesisTask']['TaskId'] + '.mp3'

    tts_task_status = tts_task_resp(polly_response['SynthesisTask']['TaskId'])

    while tts_task_status['SynthesisTask']['TaskStatus'] == 'scheduled':
        tts_task_status = tts_task_resp(polly_response['SynthesisTask']['TaskId'])
        logging.info(
            f"polly task :{polly_response['SynthesisTask']['TaskId']}, status :{tts_task_status['SynthesisTask']['TaskStatus']}")
        sleep(3)

    if tts_task_status['SynthesisTask']['TaskStatus'] == 'completed':
        logging.info(
            f"polly task :{polly_response['SynthesisTask']['TaskId']}, status :{tts_task_status['SynthesisTask']['TaskStatus']}")
    audio_url = tts_task_status['SynthesisTask']['OutputUri']
    logging.info(f"public audio link: {audio_url}")

    set_public_access_response = set_public_access(S3_BUCKET, audio_book_topic, polly_file_name, DRAFT_TOPIC)
    logging.info(f"set_public_access_response: {set_public_access_response}")

    raw_transcript = transcript_generator(description)
    logging.info(f"raw_transcript: {raw_transcript}")
    logging.info(f"generating word by word transcript ...")
    word_by_transcript = get_word_by_transcript(raw_transcript)

    logging.info(f"word_by_transcript: {word_by_transcript}")
    if not audio_url or not raw_transcript or not word_by_transcript:
        logging.error(
            f"Ran into error while generating response audio_url: {audio_url},raw_transcript: {raw_transcript},"
            f"word_by_transcript: {word_by_transcript}")
        return jsonify({"error": "Ran into error while generating response"}), 500
    return jsonify({"audio_url": audio_url, "word_by_transcript": word_by_transcript})


@app.route('/addReference', methods=['POST'])
def add_reference():
    return ''


if __name__ == '__main__':
    app.run(port=8066)
