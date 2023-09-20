import psycopg2
import psycopg2.pool
import datetime
import os
import dotenv
from stockholm_souls.secrets import generate_secret, hash_passwd
from stockholm_souls.database.validator import password_verification

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Создаем пул соединений
connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URL)

def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


def verification(uname, passwd):
    errors = {}
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{uname}'")
            info = cursor.fetchall()
            if info:
                info = password_verification(info, passwd)
                return info
        errors['login'] = 'There is no such login'
        return errors
    finally:
        release_connection(conn)


def take_user_id(uname):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE username = '{uname}'")
            id = cursor.fetchall()[0][0]
            return id
    finally:
        release_connection(conn)


def take_user_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = {id} ")
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def check_user(uname):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{uname}' ")
            if cursor.fetchall():
                return True
            return False
    finally:
        release_connection(conn)


def take_additional_user_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users_additionally WHERE id = %s", (id))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def create_new_user(name, passwd, country, gender, age):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            passwd = hash_passwd(passwd)
            current_time = datetime.datetime.now()
            fromated_time = current_time.strftime('%Y-%m-%d')
            cursor.execute("BEGIN")
            cursor.execute("INSERT INTO users (username, password, create_at) VALUES (%s, %s, %s)",
                           (name, passwd, fromated_time))
            cursor.execute("SELECT LASTVAL()")
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO users_additionally (user_id, gender, years, country) VALUES (%s, %s, %s, %s)",
                           (user_id, gender, age, country))
            secret = generate_secret(name, passwd)
            cursor.execute("INSERT INTO users_secrets (user_id, secret) VALUES (%s, %s)", (user_id, secret))

            cursor.execute("COMMIT")
    except:
        cursor.execute("ROLLBACK")
    finally:
        release_connection(conn)


def create_session_data(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = (id)")
            data = cursor.fetchall()[0]
            result_data = {
                'id': f'{data[0]}',
                'name': f'{data[1]}',
                'passwd': f'{data[1]}'
            }
            return result_data
    finally:
        release_connection(conn)



def check_valid_api_key(secret, tg_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users_secrets WHERE secret = (secret)")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"UPDATE users_secrets SET telegram_id = %s WHERE id = %s", (tg_id, data[0][0]))
                return 'успех'
            return "такого пользователя нет"
    finally:
        release_connection(conn)