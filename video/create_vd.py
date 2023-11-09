import logging
import os
import random

import moviepy.editor as mp

from utilities.const import LOG_PATH

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', filename=LOG_PATH)


class VideoProcessor:
    def __init__(self, _video_folder, _audio_file, _output_file):
        self.video_folder = _video_folder
        self.audio_file = _audio_file
        self.output_file = _output_file

    def process_video(self):
        if not self.video_folder or self.audio_file:
            logging.info("not found or audio_file")
        logging.info("Step 1: Selecting a random video")
        video_files = os.listdir(self.video_folder)
        selected_video = random.choice(video_files)
        video_path = os.path.join(self.video_folder, selected_video)

        logging.info("Step 2: Loading the audio file")
        audio = mp.AudioFileClip(self.audio_file)
        audio_duration = audio.duration

        logging.info("Step 3: Loading the video clip")
        video = mp.VideoFileClip(video_path)

        logging.info("Step 4: Resizing and cropping the video")
        target_aspect_ratio = 9 / 16
        video_aspect_ratio = video.size[0] / video.size[1]

        if video_aspect_ratio > target_aspect_ratio:
            # The video is wider, crop the sides
            target_width = video.size[1] * target_aspect_ratio
            crop_left = (video.size[0] - target_width) / 2
            crop_right = crop_left + target_width
            video = video.crop(x1=crop_left, x2=crop_right)
        else:
            # The video is taller, crop the top and bottom
            target_height = video.size[0] / target_aspect_ratio
            crop_top = (video.size[1] - target_height) / 2
            crop_bottom = crop_top + target_height
            video = video.crop(y1=crop_top, y2=crop_bottom)

        video = video.resize(width=video.w, height=video.h).set_duration(audio_duration)

        logging.info("Step 5: Setting the audio for the final video")
        final_video = video.set_audio(audio)

        logging.info("Step 6: Writing the final video")
        final_video.write_videofile(self.output_file, codec='libx264', audio_codec='aac', fps=24)

        logging.info("Video processing completed successfully.")
        return self.output_file


# # Usage example:
# video_folder = STOCK_VIDEO_FOLDER
# audio_file = "C:/YT/video/HowtoconnectaPS4controllertoaPC-16-05-2023.mp3"
# output_file = OUTPUT_TMP + "output.mp4"
#
# processor = VideoProcessor(video_folder, audio_file, output_file)
# processed_file = processor.process_video()
# print("Processed video file:", processed_file)
