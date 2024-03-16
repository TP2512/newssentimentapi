import pytest
from services import get_sentiment
from endpoints.news import get_sentiment_from_news
from fastapi import HTTPException, status
from bson import ObjectId
from unittest.mock import patch, MagicMock
import unittest


# class TestJoke(unittest.TestCase):
#     @patch("services.get_sentiment")
#     def test_get_joke(self, mock_req):
#         mock_req.return_value = 'Neutral'
#         self.assertEqual(get_sentiment_from_news(), 'Neutral')
#

@pytest.fixture
async def mock_current_user():
    return {"_id": ObjectId("65ea1ca599b9a1b3aa159dc1")}


@pytest.mark.asyncio
async def test_get_sentiment(mock_current_user):
    news_input = """The Congress-led United Democratic Front (UDF) is likely to win 14 of the 20 
    Lok Sabha seats in the upcoming Lok Sabha elections, with four seats predicted for the LDF, 
    according to the News18 Mega Opinion Poll."""
    await get_sentiment_from_news(news_input, current_user=mock_current_user)
    assert response.id == "65ea1ca599b9a1b3aa159dc1"

    with pytest.raises(HTTPException) as exc_info:
        await get_sentiment_from_news(news_input,  current_user=mock_current_user)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    # response = await get_sentiment_from_news(news_input, current_user=mock_current_user)
    # assert response.id == "65ea1ca599b9a1b3aa159dc1"
