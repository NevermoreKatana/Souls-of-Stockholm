import psycopg2
import psycopg2.pool
import datetime
import os
import dotenv
from stockholm_souls.secrets import hash_passwd
from stockholm_souls.database.validator import password_verification

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Создаем пул соединений
connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn=0, maxconn=25, dsn=DATABASE_URL)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)


def verification(uname, passwd):
    errors = {}
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = %s", (uname,))
            info = cursor.fetchall()
            if info:
                salt = info[0][3]
                passwd = hash_passwd(passwd, salt)
                info = password_verification(info, passwd['hex'])
                return info
        errors['login'] = 'There is no such login'
        return errors
    finally:
        release_connection(conn)


def take_user_id(uname):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE username = %s", (uname,))
            id = cursor.fetchall()[0][0]
            return id
    finally:
        release_connection(conn)


def take_user_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = %s", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def check_user(uname):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = %s", (uname,))
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


def create_new_user(name, passwd, country, gender, age, secret):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            passwd = hash_passwd(passwd)
            current_time = datetime.datetime.now()
            fromated_time = current_time.strftime('%Y-%m-%d')
            cursor.execute("BEGIN")
            cursor.execute("INSERT INTO users (username, password, salt, create_at) VALUES (%s, %s, %s, %s)",
                           (name, passwd['hex'], passwd['salt'], fromated_time))
            cursor.execute("SELECT LASTVAL()")
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO users_additionally (user_id, gender, years, country) VALUES (%s, %s, %s, %s)",
                           (user_id, gender, age, country))
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
            cursor.execute(f"SELECT * FROM users WHERE id = %s", (id,))
            data = cursor.fetchall()[0]
            cursor.execute(f"SELECT secret FROM users_secrets WHERE user_id = %s", (id, ))
            secret_key = cursor.fetchone()[0]
            result_data = {
                'id': data[0],
                'name': data[1],
                'passwd': data[2],
                'secret': secret_key
            }
            return result_data
    finally:
        release_connection(conn)


def take_all_posts():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts ORDER BY id")
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def take_one_post(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts WHERE id = %s", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)




def take_comments(post_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM comments WHERE post_id = %s", (post_id,))
            data = cursor.fetchall()
            return data
    finally:
        release_connection(conn)


def add_comments(post_id, content, user_data):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO comments (post_id, user_id, username, content) VALUES (%s, %s, %s, %s)", (post_id, user_data['id'],user_data['name'], content,))
            cursor.execute("COMMIT")
    finally:
        release_connection(conn)


def add_new_post(user_id, username, post_name, content):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO posts (user_id, user_name, name, content) VALUES (%s,%s,%s,%s)", (user_id, username, post_name, content))
            cursor.execute("COMMIT")
    finally:
        release_connection(conn)


def take_jwt(username):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE username = %s", (username,))
            id = cursor.fetchone()[0]
            cursor.execute(f"SELECT secret FROM users_secrets WHERE user_id = %s", (id,))
            return cursor.fetchone()[0]
    finally:
        release_connection(conn)