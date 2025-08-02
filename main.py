from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
from news_fetcher import fetch_news
from sentiment import analyze_sentiment, get_overall_sentiment
from database import Database

# Initialize app with metadata
app = FastAPI(
    title="Stock News Sentiment API",
    description="Real-time sentiment analysis for stock news headlines",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
)

db = Database()
logger = logging.getLogger(__name__)


# --- Models ---
class Headline(BaseModel):
    title: str
    sentiment: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "TCS reports record quarterly profits",
                "sentiment": "positive"
            }
        }


class SentimentResponse(BaseModel):
    symbol: str
    timestamp: str
    headlines: List[Headline]
    overall_sentiment: str

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "TCS",
                "timestamp": "2023-11-16T12:34:56.789Z",
                "headlines": [
                    {"title": "TCS expands to European market", "sentiment": "positive"},
                    {"title": "IT sector faces headwinds", "sentiment": "negative"}
                ],
                "overall_sentiment": "neutral"
            }
        }


# --- Endpoints ---
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Service health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "operational",
            "news_fetcher": "ready",
            "sentiment_analyzer": "ready"
        }
    }


@app.post(
    "/news-sentiment",
    response_model=SentimentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "No news found for the given symbol"},
        500: {"description": "Internal server error"}
    }
)
async def analyze_stock_sentiment(symbol: str):
    """
    Analyze sentiment for stock news headlines

    - **symbol**: Stock ticker symbol (e.g. "TCS")
    - Returns: Analyzed headlines with sentiment scores
    """
    try:
        # Check cache first
        if cached := db.get_cached(symbol):
            logger.info(f"Serving cached result for {symbol}")
            return cached

        # Fetch and analyze news
        headlines = fetch_news(symbol)
        if not headlines:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No news found for symbol {symbol}"
            )

        analyzed = [
            {"title": h, "sentiment": analyze_sentiment(h)}
            for h in headlines
        ]

        response = {
            "symbol": symbol.upper(),
            "timestamp": datetime.utcnow().isoformat(),
            "headlines": analyzed,
            "overall_sentiment": get_overall_sentiment([h["sentiment"] for h in analyzed])
        }

        db.cache_result(response)
        return response


    except Exception as e:

        import traceback

        traceback.print_exc()  # <-- Add this line to print full error in console

        logger.error(f"Error processing {symbol}: {str(e)}")

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=f"Internal server error: {str(e)}"  # <-- Temporarily expose error

        )


# --- OpenAPI Customization ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Stock News Sentiment API",
        version="1.0.0",
        description="Professional-grade API for stock news analysis",
        routes=app.routes,
    )

    # Add more customization if needed
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi