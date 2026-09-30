import pytest
from .core import analyze_code, cache_analysis_result, get_analysis_result

@pytest.fixture
async def setup_db():
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        result TEXT
    )
    ''')
    yield conn
    conn.close()

def test_analyze_code(setup_db):
    result = analyze_code('test.py')
    assert result == 'Dead code found'  # Assuming 'dead code' is in the test file

@pytest.mark.asyncio
async def test_cache_analysis_result(setup_db):
    filename = 'test.py'
    result = 'Dead code found'
    cache_analysis_result(filename, result)
    assert get_analysis_result(filename) == result