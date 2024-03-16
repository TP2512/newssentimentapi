from fastapi import HTTPException, status, Depends, APIRouter
from utils import oauth2
from models import schema as sc
from services import get_sentiment as gs
from loggers import configure_logger


logger = configure_logger()
router = APIRouter()


@router.post("/get_sentiment_from_news", response_model=sc.NewsResponse, status_code=status.HTTP_200_OK)
async def get_sentiment_from_news(news: sc.NewsInput, current_user: dict = Depends(oauth2.get_current_user)):
    try:
        senti_getter = gs.SentimentAnalysis(news.news_article)
        senti_of_news = senti_getter.get_sentiment_from_app()
        logger.info(f"SA response to user:{str(current_user['_id'])}")
        return sc.NewsResponse(sentiment=senti_of_news)
    except Exception as e:
        logger.critical(f"Getting issue with sentiment analysis web app:{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
