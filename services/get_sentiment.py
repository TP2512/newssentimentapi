import requests as rq
from loggers import configure_logger


logger = configure_logger()


class SAError(Exception):
    def __init__(self, message="Bad Request to Sentiment Web Server"):
        self.message = message
        super().__init__(self.message)


class SentimentAnalysis:
    def __init__(self, news):
        self.news = news
        self._url = "http://127.0.0.1:8001/get_sentiment"

    def get_sentiment_from_app(self):
        try:
            response = rq.post(self._url, json={"news_article": self.news})
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"sentiment analysis app {response.status_code} ")
                raise SAError("Bad Request to Sentiment Web Server")
        except Exception as e:
            logger.error(f"Sentiment analysis app facing issue {e}")
            return e
