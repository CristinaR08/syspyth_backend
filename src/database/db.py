import psycopg2
from psycopg2.extras import RealDictCursor
from config import config

def get_db_connection():
    db_uri = config['development'].DATABASE_URI
    connection = psycopg2.connect(db_uri)
    return connection

def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()

def fetch_all(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def fetch_one(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
