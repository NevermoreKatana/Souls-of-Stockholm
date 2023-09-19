import psycopg2
import datetime
import os
import dotenv
from stockholm_souls.database.validator import password_verification

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def take_user_info(uname, passwd):
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