import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import config
import psycopg2

def create_table():
    connection = psycopg2.connect(
        host=config['development'].PGSQL_HOST,
        user=config['development'].PGSQL_USER,
        password=config['development'].PGSQL_PASSWORD,
        database=config['development'].PGSQL_DATABASE
    )
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS estudiantes (
        cedula VARCHAR(10) PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NOT NULL,
        carrera VARCHAR(100) NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_table()
