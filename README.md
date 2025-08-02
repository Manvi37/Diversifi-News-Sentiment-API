# 📰 News Sentiment API

This FastAPI service fetches news headlines for a given Indian stock symbol, performs sentiment analysis, stores results in a local SQLite DB, and returns the response via API.

## 🚀 Features
- ✅ Fetches latest headlines from Google News RSS
- ✅ Performs sentiment analysis using TextBlob
- ✅ Stores results in SQLite

## 🛠 Tech Stack
- FastAPI
- feedparser
- NLTK (VADER)
- SQLite (via SQLAlchemy)
- Uvicorn

## Use of AI Tools
To speed up development while maintaining original design and structure:
- ChatGPT was used for debugging (e.g., fixing coroutine serialization issues), validating logic, and suggesting improvements for handling edge cases.
- DeepSeek was used to assist with boilerplate generation and to accelerate implementation of certain FastAPI components.

## 📦 Installation

```bash
pip install -r requirements.txt
uvicorn main:app --reload
