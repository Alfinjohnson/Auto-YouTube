
import logging

from tts.polly import AudioProcessor
from utilities.const import TECH_NEWS, LOG_PATH
from topic.news import NEWS

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', filename=LOG_PATH)


class ExtractNews:
    def __init__(self, news_url):
        self.url = news_url
        self.generated_files = []

    @property
    def process_data(self):
        try:
            news = NEWS(self.url)
            news_response = news.getnews()
            logging.info(f"news_response: {news_response}")
            logging.info(f"fetched article length news_response: {len(news_response)}")
            for article in news_response:
                title = article.get("title")
                description = article.get("description")
                link = article.get("link")
                category = article.get("category")
                keywords = article.get("keywords")
                logging.info(
                    f"title:{title} description :{description}, link :{link}, category :{category},keywords :{keywords}")
                try:
                    self.polly_tts(title, description, link, category, keywords)
                except Exception as e:
                    logging.error(f"Error occurred during rephrasing: {e}")
        except Exception as e:
            logging.error(f"Error occurred during news extraction: {e}")
        return self.generated_files

    def polly_tts(self, title, description, link, category, keywords):
        logging.info(f"inside polly_tts method title: {title} ,description: {description} ")
        audio_processor = AudioProcessor(title, description)
        audio_file_name = audio_processor.synthesize_speech()
        transcript_file_name = audio_processor.generate_transcript()
        json_obj = {"audio_file_name": audio_file_name, "transcript_file_name": transcript_file_name, "link": link,
                    "category": category, "keywords": keywords, "title": title}
        logging.info(f"json_obj: {json_obj}")
        self.generated_files.append(json_obj)
