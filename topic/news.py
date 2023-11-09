import logging
import requests

from utilities.const import NEWS_FETCH_LIMIT, LOG_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_PATH)


class NEWS:
    def __init__(self, news_url):
        self.news_fetch_limit = NEWS_FETCH_LIMIT
        self.url = news_url

    def getnews(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response_data = response.json()
            response_business = response_data["results"][:self.news_fetch_limit]
            logging.info("API request successful. Retrieved {} business news articles.".format(len(response_business)))
            return response_business
        except requests.exceptions.RequestException as e:
            logging.error("API request failed: {}".format(str(e)))
