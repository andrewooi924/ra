import sqlite3

DB_NAME = "search_history.db"

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_search(query, results):
    """Save search query and results to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO searches (query, results) VALUES (?, ?)", (query, results))
    conn.commit()
    conn.close()

def get_search_history(limit=5):
    """Retrieve the last few searches from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT query, results FROM searches ORDER BY id DESC LIMIT ?", (limit,))
    history = cursor.fetchall()
    conn.close()
    return history
