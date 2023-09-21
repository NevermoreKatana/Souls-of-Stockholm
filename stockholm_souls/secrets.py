import os

import bcrypt
import dotenv
dotenv.load_dotenv()

ROUNDS = int(os.getenv('ROUNDS'))
DESIRED_KEY_BYTES = int(os.getenv('DESIRED_KEY_BYTES'))

def hash_passwd(passwd, salt=''):
    encoded_passwd = passwd.encode('utf-8')
    if salt == '':
        salt = bcrypt.gensalt()
    else:
        salt = bytes.fromhex(salt)
    secret_passwd = bcrypt.kdf(encoded_passwd, salt, desired_key_bytes=DESIRED_KEY_BYTES, rounds=ROUNDS)

    secret_passwd_hex = secret_passwd.hex()
    password_data = {
        'hex': secret_passwd_hex,
        'salt': salt.hex()
    }
    return password_data
