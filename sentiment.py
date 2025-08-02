from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "positive"
    elif analysis.sentiment.polarity < -0.1:
        return "negative"
    return "neutral"

def get_overall_sentiment(sentiments: list) -> str:
    if not sentiments:
        return "neutral"  # or "unknown"
    return max(set(sentiments), key=sentiments.count)
