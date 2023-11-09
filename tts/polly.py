import json
import boto3
import logging
import re

from utilities.const import get_current_date, AWS_ACCESS_KEY, AWS_SEC_KEY, OUTPUT_AUDIO, OUTPUT_TRANSCRIPT, \
    LOG_PATH

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', filename=LOG_PATH)


class AudioProcessor:
    def __init__(self, _title, _description):
        logging.info(f"AudioProcessor class  {_title} , {_description}")
        self.title = _title
        self.text = _description
        substring_title = re.sub('[^A-Za-z0-9]+', '', self.title)
        current_time = get_current_date()
        self.file_name = f"{substring_title}-{current_time}"

        self.polly_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SEC_KEY,
            region_name='ap-south-1'
        ).client('polly')

    def synthesize_speech(self):
        try:
            logging.info(f"inside synthesize_speech")
            audio_response = self.polly_client.synthesize_speech(
                OutputFormat='mp3',
                Text=self.text,
                VoiceId='Joanna',
                Engine='standard'
            )

            with open(OUTPUT_AUDIO + self.file_name + '.mp3', 'wb') as file:
                file.write(audio_response['AudioStream'].read())
                logging.info(f"audio_response {audio_response}")
            return OUTPUT_AUDIO + self.file_name + '.mp3'
        except Exception as e:
            logging.error(f"Error occurred during speech synthesis: {e}")

    def generate_transcript(self):
        try:
            marks_response = self.polly_client.synthesize_speech(
                OutputFormat='json',
                Text=self.text,
                VoiceId='Joanna',
                SpeechMarkTypes=['word'],
                Engine='standard',
            )

            marks = json.loads(
                '[' + marks_response['AudioStream'].read().decode('utf-8').replace('}\n{', '},\n{') + ']')
            transcript = []
            for mark in marks:
                start_time = mark['time'] / 1000
                sentence = mark['value']
                transcript.append({
                    'start_time': start_time,
                    'sentence': sentence
                })

            with open(OUTPUT_TRANSCRIPT + self.file_name + '.json', 'w') as file:
                json.dump(transcript, file, indent=4)
            return OUTPUT_TRANSCRIPT + self.file_name + '.json'
        except Exception as e:
            logging.error(f"Error occurred during transcript generation: {e}")

# title = "Edett 23"
# description = "Sentinels have announced a partnership with Starforge Systems, the PC building company founded by OTK and MoistCr1TiKaL."
# audio_processor = AudioProcessor(title, description)
#
# audio_processor.synthesize_speech()
# audio_processor.generate_transcript(text)
