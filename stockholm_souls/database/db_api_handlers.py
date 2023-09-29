from stockholm_souls.database.db_conn import get_connection, release_connection

checks = {
    'success': {
        'answer':
            'Проверка прошла успешно телеграмм успешно привязан к аккаунту',
        'status_code': 'authorized'
    },
    'denied': {
        'answer': 'Проверка провалена, телеграм не привязан к аккаунту',
        'status_code': 'not authorized'
    }
}


def add_new_comment(jwt, post_id, content):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("BEGIN")

            cursor.execute("""
                    INSERT INTO comments (post_id, user_id, username, content)
                    SELECT %s, user_id, username, %s
                    FROM users_secrets
                    JOIN users ON users_secrets.user_id = users.id
                    WHERE secret = %s
                """, (post_id, content, jwt))

            cursor.execute("COMMIT")

    finally:
        release_connection(conn)


def check_valid_jwt_key(secret, tg_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users_secrets WHERE secret = %s", (secret,))
            data = cursor.fetchall()
            if data:
                cursor.execute("UPDATE users_secrets SET telegram_id = %s WHERE user_id = %s", (tg_id, data[0][0]))
                cursor.execute("COMMIT")
                return checks['success']
            return checks['denied']
    finally:
        release_connection(conn)


def take_posts_api(jwt):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users_secrets WHERE secret = %s", (jwt,))
            data = cursor.fetchall()
            if data:
                cursor.execute("SELECT * FROM posts ORDER BY id ")
                return cursor.fetchall()
    finally:
        release_connection(conn)


def take_one_post_api(id):
    result = {}
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
            data = cursor.fetchall()
            result['post_data'] = data
            cursor.execute("SELECT * FROM comments WHERE post_id = %s", (id,))
            data = cursor.fetchall()
            result['comment'] = data
            return result
    finally:
        release_connection(conn)


def create_new_post(jwt, post_name, content):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("BEGIN")
            cursor.execute("SELECT user_id FROM users_secrets WHERE secret = %s", (jwt,))
            id = cursor.fetchone()[0]
            cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
            username = cursor.fetchone()[0]
            cursor.execute("INSERT INTO posts (user_id, user_name, name, content) VALUES (%s,%s,%s,%s)", (id, username, post_name, content))
            cursor.execute("COMMIT")
            return '0'
    finally:
        release_connection(conn)


def check_valid_jwt(jwt):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("BEGIN")
            cursor.execute("SELECT * FROM users_secrets WHERE secret = %s", (jwt,))
            data = cursor.fetchall()
            if data:
                return True
            return False
    finally:
        release_connection(conn)


def take_jwt(username):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            id = cursor.fetchone()[0]
            cursor.execute("SELECT secret FROM users_secrets WHERE user_id = %s", (id,))
            return cursor.fetchone()[0]
    finally:
        release_connection(conn)
