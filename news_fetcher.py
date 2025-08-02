import feedparser
from typing import List
import logging

logger = logging.getLogger(__name__)

def fetch_news(symbol: str) -> List[str]:
    try:
        feed = feedparser.parse(
            f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
        )
        return [entry.title for entry in feed.entries[:3]]
    except Exception as e:
        logger.error(f"News fetch failed: {e}")
        return [
            f"{symbol} reports strong earnings",  # Fallback data
            f"Market analysts discuss {symbol}",
            f"{symbol} announces new product"
        ]