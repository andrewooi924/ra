import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/research_assistant") 

def connect_db():
    return psycopg2.connect(DATABASE_URL)

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