import os
from hashlib import pbkdf2_hmac
import bcrypt
import dotenv
dotenv.load_dotenv()

ROUNDS = int(os.getenv('ROUNDS'))


def hash_passwd(passwd, salt=''):
    encoded_passwd = passwd.encode('utf-8')
    if salt == '':
        salt = bcrypt.gensalt()
    else:
        salt = bytes.fromhex(salt)
    secret_passwd = pbkdf2_hmac('sha256', encoded_passwd, salt, ROUNDS)

    secret_passwd_hex = secret_passwd.hex()
    password_data = {
        'hex': secret_passwd_hex,
        'salt': salt.hex()
    }
    return password_data
