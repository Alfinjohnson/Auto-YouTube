import moviepy.editor as mp
import logging
import cv2
import json

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class VideoTextOverlay:
    def __init__(self, _video_path, _json_path):
        self.video_path = _video_path
        self.json_path = _json_path

    def add_text_overlay(self, _output_path):
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        with open(self.json_path) as json_file:
            data = json.load(json_file)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(_output_path, fourcc, fps, (width, height))

        current_text = ""
        current_index = 0
        combined_sentences = []

        for frame_index in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
            ret, frame = video.read()
            if not ret:
                break

            current_time = frame_index / fps

            while current_index < len(data) and data[current_index]["start_time"] <= current_time:
                combined_sentences.append(data[current_index]["sentence"])
                current_index += 1

            if len(combined_sentences) > 3:
                combined_sentences = combined_sentences[-3:]  # Keep the last three sentences

            current_text = " ".join(combined_sentences)

            # Split long text into multiple lines if it doesn't fit within the video frame
            words = current_text.split()
            lines = []
            current_line = ""
            for word in words:
                if cv2.getTextSize(current_line + " " + word, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][0] > width:
                    lines.append(current_line.strip())
                    current_line = word
                else:
                    current_line += " " + word
            lines.append(current_line.strip())

            # Calculate the position to center the text in the video frame
            line_height = cv2.getTextSize(current_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][1]
            text_y = int((height - line_height * len(lines)) / 2)

            # Draw each line of the text with black background and white stroke
            for line in lines:
                text_size, _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                text_x = int((width - text_size[0]) / 2)
                text_y += line_height

                # Add padding to the background rectangle
                padding = 10
                background_height = int(line_height * 1.2)
                background_width = text_size[0] + 2 * padding
                background_top = text_y - background_height - padding
                background_bottom = text_y + padding

                # Add black background to the text
                cv2.rectangle(frame, (text_x - padding, background_top),
                              (text_x + background_width, background_bottom), (0, 0, 0), -1)

                # Add white stroke to the text
                cv2.putText(frame, line, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            output_video.write(frame)
        video.release()
        output_video.release()
        return _output_path


# # Example usage
# video_path = OUTPUT_TMP + "output.mp4"
# json_path = OUTPUT_TRANSCRIPT + "HowtoconnectaPS4controllertoaPC-16-05-2023.json"
# output_path = OUTPUT_FINAL_VIDEO + "output_video.mp4"
#
# # overlay = VideoTextOverlay(video_path, json_path)
# # output_path = overlay.add_text_overlay(output_path)
# # print("Text overlay added successfully!")
# # print("Output video path:", output_path)


class AddAudio:
    def __init__(self, _video_path, audio_file, output_file):
        self.video_folder = _video_path
        self.audio_file = audio_file
        self.output_file = output_file

    def process_audio(self):
        logging.info("Step 2: Loading the audio file")
        audio = mp.AudioFileClip(self.audio_file)

        logging.info("Step 3: Loading the video clip")
        video = mp.VideoFileClip(self.video_folder)

        logging.info("Step 5: Setting the audio for the final video")
        final_video = video.set_audio(audio)

        logging.info("Step 6: Writing the final video")
        final_video.write_videofile(self.output_file, codec='libx264', audio_codec='aac', fps=24)

        logging.info("add audio processing completed successfully.")
        return self.output_file


# Usage example:
# video_path = output_path
# audio_file = "res/audio/HowtoconnectaPS4controllertoaPC-16-05-2023.mp3"
# output_file = "output/final.mp4"
#
# processor = AddAudio(video_path, audio_file, output_file)
# processed_file = processor.process_audio()
# print("Processed video file:", processed_file)
