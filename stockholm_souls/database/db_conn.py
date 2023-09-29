import psycopg2
import psycopg2.pool
import datetime
import os
import dotenv
dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Создаем пул соединений
connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn=0, maxconn=25, dsn=DATABASE_URL)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)



