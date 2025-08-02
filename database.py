import sqlite3
from datetime import datetime, timedelta
import json


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('news.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                symbol TEXT,
                timestamp TEXT,
                headlines TEXT,
                sentiments TEXT
            )
        ''')
        self.conn.commit()

    def get_cached(self, symbol: str):
        self.cursor.execute('''
            SELECT * FROM news 
            WHERE symbol = ? 
            AND timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (symbol, (datetime.utcnow() - timedelta(minutes=10)).isoformat()))

        if row := self.cursor.fetchone():
            return {
                "symbol": row[1],
                "timestamp": row[2],
                "headlines": [
                    {"title": t, "sentiment": s}
                    for t, s in zip(json.loads(row[3]), json.loads(row[4]))
                ],
                "overall_sentiment": max(set(json.loads(row[4])), key=json.loads(row[4]).count)  # Majority vote
            }
        return None

    def cache_result(self, data: dict):
        self.cursor.execute('''
            INSERT INTO news (symbol, timestamp, headlines, sentiments)
            VALUES (?, ?, ?, ?)
        ''', (
            data["symbol"],
            data["timestamp"],
            json.dumps([h["title"] for h in data["headlines"]]),
            json.dumps([h["sentiment"] for h in data["headlines"]])
        ))
        self.conn.commit()