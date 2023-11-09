import logging
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta

from utilities.const import CHANNEL_ID, YT_SECRET_FILE, LOG_PATH, SCOPES

# Configure logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', filename=LOG_PATH)


class YouTubeUploader:
    def __init__(self, video_file, channel_id, _YT_SECRET_FILE, _SCOPES):
        self.video_file = video_file
        self.channel_id = channel_id
        self.CLIENT_SECRET_FILE = _YT_SECRET_FILE
        self.SCOPES = SCOPES

        self.video_title = 'My Video Title'
        self.video_description = 'My Video Description'
        self.video_tags = ['tag1', 'tag2', 'tag3']
        self.video_category = '22'  # See https://developers.google.com/youtube/v3/docs/videoCategories/list

    def get_authenticated_service(self):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(self.CLIENT_SECRET_FILE,
                                                                                      self.SCOPES)
        service = build('youtube', 'v3', credentials=credentials)
        return service

    def upload_video(self):
        service = self.get_authenticated_service()
        # Upload video
        media = MediaFileUpload(self.video_file)
        self.logger.info('Uploading video...')
        request = service.videos().insert(
            part='snippet,status',
            body={
                'snippet': {
                    'title': self.video_title,
                    'description': self.video_description,
                    'tags': self.video_tags,
                    'categoryId': self.video_category,
                    'channelId': self.channel_id
                },
                'status': {
                    'privacyStatus': 'private'
                }
            },
            media_body=media
        )
        response = request.execute()
        video_id = response['id']
        self.logger.info('Video uploaded successfully!')

        # Set publish time to 10 minutes from now
        publish_time = datetime.utcnow() + timedelta(minutes=10)
        publish_time_str = publish_time.isoformat() + 'Z'
        self.logger.info('Setting publish time to: {}'.format(publish_time_str))

        # Save as draft with the specified publish time
        self.logger.info('Saving video as a draft...')
        request = service.videos().update(
            part='status',
            body={
                'id': video_id,
                'status': {
                    'privacyStatus': 'unlisted',
                    'selfDeclaredMadeForKids': False,
                    'publishAt': publish_time_str
                }
            }
        )
        request.execute()
        self.logger.info('Video saved as a draft.')


def main():
    # TODO set up function call from yt_auto_main.py
    video_file = '/YT/final/Howtoinstallanm2SSD.mp4'

    uploader = YouTubeUploader(video_file, CHANNEL_ID, YT_SECRET_FILE, SCOPES)
    uploader.upload_video()


if __name__ == '__main__':
    main()
