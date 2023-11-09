import json

import boto3
from botocore.config import Config

from utilities.const import AWS_ACCESS_KEY, AWS_SEC_KEY, get_current_date, S3_BUCKET

my_config = Config(
    region_name='ap-south-1',
    signature_version='v4',
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)

client = boto3.client('polly', config=my_config,
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SEC_KEY,
                      )


def polly(audio_book_name, audio_content, topic_type):
    response = client.start_speech_synthesis_task(
        Engine='neural',
        LanguageCode='en-IN',
        OutputFormat='mp3',
        OutputS3BucketName=S3_BUCKET,
        OutputS3KeyPrefix=topic_type + '/' + get_current_date() + '/' + audio_book_name,
        SampleRate='16000',
        Text=audio_content,
        TextType='text',
        VoiceId='Joanna',
        SpeechMarkTypes=['word']
    )
    return response


def tts_task_resp(task_id):
    response = client.get_speech_synthesis_task(
        TaskId=task_id
    )
    return response


def transcript_generator(contents):
    marks_response = client.synthesize_speech(
        OutputFormat='json',
        Text=contents,
        VoiceId='Joanna',
        # sentence | ssml | viseme | word
        SpeechMarkTypes=['word']
    )
    raw_transcript = json.loads(
        '[' + marks_response['AudioStream'].read().decode('utf-8').replace('}\n{', '},\n{') + ']')
    return raw_transcript


def get_word_by_transcript(raw_transcript):
    # Generate the transcript
    transcript = []
    for mark in raw_transcript:
        start_time = mark['time'] / 1000
        sentence = mark['value']
        transcript.append({
            'start_time': start_time,
            'sentence': sentence
        })
    return transcript
