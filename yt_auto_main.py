import json
import logging
import os
import re

from processing.extract_topic import ExtractNews
from utilities.const import (
    LOG_PATH,
    STOCK_VIDEO_FOLDER,
    OUTPUT_TMP,
    OUTPUT_FINAL_VIDEO,
    OUTPUT_FINAL_INFO,
    get_current_date,
    NEWS_API_KEY,
    EXISTING_TOPICS,
)
from utilities.create_directories import create_directories
from video.create_vd import VideoProcessor
from video.subtitle import VideoTextOverlay, AddAudio


class MultiLogger:
    def __init__(self, name, file_path, log_to_console=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # File Handler
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console Handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        # create project directories mention
        create_directories()

    def get_logger(self):
        return self.logger


logger = MultiLogger("AutoYT", LOG_PATH).get_logger()


def _news(news_api):
    news_extractor = ExtractNews(news_api)
    generated_files_response = news_extractor.process_data
    logger.info(f"generated_files_response {generated_files_response}")
    generate_video(generated_files_response)


def generate_video(generated_files_response):
    final_json = []
    for item in generated_files_response:
        audio_file_name = item["audio_file_name"]
        transcript_file_name = item["transcript_file_name"]
        if audio_file_name or transcript_file_name:
            logger.info("transcript_file_name or transcript_file_name not found")
            link = item.get("link", [])
            category = item["category"]
            keywords = item.get("keywords", [])
            title = item.get("title", [])
            logger.info(f"Audio File Name:{audio_file_name}")
            logger.info(f"Transcript File Name:{transcript_file_name}")
            logger.info(f"Link:{link}")
            logger.info(f"Category:{category}")
            logger.info(f"Keywords:{keywords}")
            logger.info(f"title:{title}")

            re_title = re.sub('[^A-Za-z0-9]+', '', title)
            if check_and_add_topic(re_title, EXISTING_TOPICS):
                logger.info(f"topic already exist:{title}")
            else:
                create_video_output_file = OUTPUT_TMP + re_title + ".mp4"
                processor = VideoProcessor(STOCK_VIDEO_FOLDER, audio_file_name, create_video_output_file)
                video_path = processor.process_video()
                logger.info(f"Processed video file:{video_path}")

                output_subtitle_filename = OUTPUT_TMP + re_title + "-subtitle.mp4"
                overlay = VideoTextOverlay(video_path, transcript_file_name)
                output_subtitle_filename_response = overlay.add_text_overlay(output_subtitle_filename)

                logger.info("Text overlay added successfully!")
                logger.info(f"Output video path:{output_subtitle_filename_response}")

                output_file_final = OUTPUT_FINAL_VIDEO + re_title + ".mp4"
                processor = AddAudio(output_subtitle_filename_response, audio_file_name, output_file_final)
                processed_file = processor.process_audio()
                logger.info(f"Processed video file:{processed_file}")

                final_video_json = {
                    "audio_file_name": item["audio_file_name"],
                    "transcript_file_name": item["transcript_file_name"],
                    "link": item["link"],
                    "category": item["category"],
                    "keywords": item["keywords"],
                    "title": item["title"],
                }

                if keywords is not None:
                    updated_keywords = ' '.join(['#' + topic for topic in keywords])
                else:
                    updated_keywords = ''
                if title is not None:
                    updated_keywords += "\n" + title
                #                if link is not None:
                #                    updated_keywords += "\n article link " + link

                final_video_json["yt_description"] = updated_keywords
                final_json.append(final_video_json)

    logger.info(f"final_json Processed video :{final_json}")
    with open(OUTPUT_FINAL_INFO + 'video-info-' + get_current_date() + ".json", "w") as outfile:
        json.dump(final_json, outfile, indent=4)
    logger.info(f"Task completed ...")


def check_and_add_topic(new_topic, existing_topics_file):
    exist_file = False

    if not os.path.exists(existing_topics_file):
        topics = []
    else:
        with open(existing_topics_file) as file:
            topics = json.load(file)

    if new_topic in topics:
        logger.info(f"Skipping '{new_topic}' as it already exists.")
        exist_file = True
    else:
        topics.append(new_topic)
        logger.info(f"Added new topic: '{new_topic}'")
        exist_file = False

    with open(existing_topics_file, 'w') as file:
        json.dump(topics, file)

    return exist_file


if __name__ == "__main__":
    logger.info(f"####.................. Service starting .................######")
    # tech topic's tech_topics = ["elon musk", "apple", "iphone 15", "amazon", "google", "chatgpt", "ai",
    # "technologies", "ticktok","instagram", "news", "smartphone", "microsoft", "meta", "metaverse","new game
    # release", "new features", " "] tech_topics = ["elon musk", "iphone", "game", " "] for tp in tech_topics:
    # logger.info(f"current tech topic processing: '{tp}'") tech_news: str = "https://newsdata.io/api/1/news?apikey="
    # + NEWS_API_KEY + "&q=" + tp + "&language=en&category=technology" _news(tech_news) # business topic's #
    # bs_topics = ["economy", "apple", "iphone 15", "amazon", "google", "chatgpt", "ai","upcoming", " ", "news",
    # "business", "USA", "london", "canada", "india", "EY", "global", "microsoft","new"] bs_topics = [" "] for tp in
    # bs_topics: logger.info(f"current business topic processing: '{tp}'") tech_news: str =
    # "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=" + tp + "&language=en&category=business" _news(
    # tech_news) # entertainment topic's # entertainment_topics = [" ", "marvel movies", "DC movies", "new movies",
    # "upcoming", "music", "harry styles"] entertainment_topics = [" "] for tp in entertainment_topics: logger.info(
    # f"current entertainment topic processing: '{tp}'") entertainment_news: str =
    # "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=" + tp + "&language=en&category=business" _news(
    # entertainment_news)
    # Daily run
    # daily_topics = ["ai", "chatgpt"]
    # for tp in daily_topics:
    #     logger.info(f"current entertainment topic processing: '{tp}'")
    #     daily_news: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=" + tp + "&language=en"
    #     _news(daily_news)

    # top topic's
    top_topics = ["ai"]
    for tp in top_topics:
        logger.info(f"current top topic's processing: '{tp}'")
        top_news: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=" + tp + "&language=en&category=top"
        _news(top_news)
    logger.info(f"####.................. Service Ended Successfully .................######")
