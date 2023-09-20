import os

import bcrypt
import dotenv
dotenv.load_dotenv()

ROUNDS = int(os.getenv('ROUNDS'))
DESIRED_KEY_BYTES = int(os.getenv('DESIRED_KEY_BYTES'))


def generate_secret(password, username):
    encoded = (username + password).encode('utf-8')

    salt = bcrypt.gensalt()
    secret_key = bcrypt.kdf(encoded, salt, desired_key_bytes=DESIRED_KEY_BYTES, rounds=ROUNDS)

    secret_key_hex = secret_key.hex()
    return secret_key_hex

def hash_passwd(passwd):
    encoded_passwd = passwd.encode('utf-8')

    salt = bcrypt.gensalt()
    secret_passwd = bcrypt.kdf(encoded_passwd, salt, desired_key_bytes=DESIRED_KEY_BYTES, rounds=ROUNDS)

    secret_passwd_hex = secret_passwd.hex()
    return secret_passwd_hex
