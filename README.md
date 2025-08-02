# 📰 News Sentiment API

This FastAPI service fetches news headlines for a given Indian stock symbol, performs sentiment analysis, stores results in a local SQLite DB, and returns the response via API.

## 🚀 Features
- ✅ Fetches latest headlines from Google News RSS
- ✅ Performs sentiment analysis using VADER (NLTK)
- ✅ Stores results in SQLite
- ✅ Caches results for 10 minutes

## 🛠 Tech Stack
- FastAPI
- feedparser
- NLTK (VADER)
- SQLite (via SQLAlchemy)
- Uvicorn

## 📦 Installation

```bash
pip install -r requirements.txt
uvicorn main:app --reload
