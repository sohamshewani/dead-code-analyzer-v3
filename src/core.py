from astroid import parse
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'cache.db')

def create_db_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        result TEXT
    )
    ''')
    conn.commit()
    return conn


def analyze_code(filename: str) -> str:
    with open(filename, 'r') as file:
        code = file.read()
        ast = parse(code)
        # Dummy logic for detecting dead code
        result = 'Dead code found' if 'dead code' in code else 'No dead code'
        return result


def cache_analysis_result(filename: str, result: str):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO analysis (filename, result) VALUES (?, ?)
    ''', (filename, result))
    conn.commit()
    conn.close()


def get_analysis_result(filename: str) -> str:
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT result FROM analysis WHERE filename = ?
    ''', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'Not cached'
