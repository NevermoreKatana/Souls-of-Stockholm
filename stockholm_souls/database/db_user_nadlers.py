from stockholm_souls.database.db_conn import get_connection, release_connection
from stockholm_souls.secrets import hash_passwd
from stockholm_souls.database.validator import password_verification
import datetime


def verification(uname, passwd):
    errors = {}
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (uname,))
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
            cursor.execute("SELECT id FROM users WHERE username = %s", (uname,))
            id = cursor.fetchall()[0][0]
            return id
    finally:
        release_connection(conn)


def take_user_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def take_additional_user_info(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users_additionally WHERE id = %s", (id))
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
    except Exception:
        cursor.execute("ROLLBACK")
    finally:
        release_connection(conn)


def create_session_data(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            data = cursor.fetchall()[0]
            cursor.execute("SELECT secret FROM users_secrets WHERE user_id = %s", (id, ))
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


def check_user(uname):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (uname,))
            if cursor.fetchall():
                return True
            return False
    finally:
        release_connection(conn)
