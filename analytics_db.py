import sqlite3
import datetime
import json

DB_FILE = 'analytics.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(query: str, response: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO queries (timestamp, query, response) VALUES (?, ?, ?)',
              (datetime.datetime.now().isoformat(), query, response))
    conn.commit()
    conn.close()

def get_total_queries():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM queries')
    total = c.fetchone()[0]
    conn.close()
    return total

def get_frequent_words():
    # Simple word frequency from queries to simulate 'frequently asked questions'
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT query FROM queries')
    rows = c.fetchall()
    conn.close()

    word_counts = {}
    for row in rows:
        words = row[0].lower().replace("?", "").replace(".", "").split()
        for w in words:
            if len(w) > 3:
                word_counts[w] = word_counts.get(w, 0) + 1

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return sorted_words

def get_recent_queries(limit=5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT timestamp, query FROM queries ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [ {"timestamp": r[0], "query": r[1]} for r in rows ]
