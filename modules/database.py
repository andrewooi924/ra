import psycopg2
import os

DATABASE_URL = "postgresql://andrewooi@localhost:5432/postgres"

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def store_search(query):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO searches (query) VALUES (%s)", (query,))
    conn.commit()
    cursor.close()
    conn.close()

def get_search_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT query, timestamp FROM searches ORDER BY timestamp DESC LIMIT 10")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results