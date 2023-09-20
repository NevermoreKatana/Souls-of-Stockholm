import psycopg2
import datetime
import os
import dotenv
from stockholm_souls.secrets import generate_secret
from stockholm_souls.database.validator import password_verification

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def verification(uname, passwd):
    errors = {}
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{uname}'")
            info = cursor.fetchall()
            if info:
                info = password_verification(info, passwd)
                return info
    errors['login'] = 'There is no such login'
    return errors


def take_user_id(uname):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE username = '{uname}'")
            id = cursor.fetchall()[0][0]
            return id



def take_user_info(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = {id} ")
            info = cursor.fetchall()
            return info

def check_user(uname):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{uname}' ")
            if cursor.fetchall():
                return True
            return False


def take_additional_user_info(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users_additionally WHERE id = {id} ")
            info = cursor.fetchall()
            return info


def create_new_user(name, passwd, country, gender, age):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            current_time = datetime.datetime.now()
            fromated_time = current_time.strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO users (username, password, create_at) VALUES (%s, %s, %s)", (name, passwd, fromated_time))
            conn.commit()
            id = take_user_id(name)
            cursor.execute("INSERT INTO users_additionally (user_id, gender, years, country) VALUES (%s, %s, %s, %s)", (id, gender, age, country))
            conn.commit()
            secret = generate_secret(name, passwd)
            cursor.execute("INSERT INTO users_secrets (user_id, secret) VALUES (%s, %s)",
                           (id, secret))
            conn.commit()


def create_session_data(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE id = (id)")
            data = cursor.fetchall()[0]
            result_data = {
                'id': f'{data[0]}',
                'name': f'{data[1]}',
                'passwd': f'{data[1]}'
            }
            return result_data



def check_valid_api_key(secret, tg_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users_secrets WHERE secret = (secret)")
            data = cursor.fetchall()
            if data:
                cursor.execute(f"UPDATE users_secrets SET telegram_id = %s WHERE id = %s", (tg_id, data[0][0]))
                return 'успех'
            return "такого пользователя нет"