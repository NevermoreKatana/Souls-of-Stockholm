from stockholm_souls.database.db import get_connection, release_connection

checks = {
    'success' : {
        'answer': 'Проверка прошла успешно телеграмм успешно привязан к аккаунту',
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
            cursor.execute("BEGIN TRANSACTION")

            cursor.execute("""
                    INSERT INTO comments (post_id, user_id, username, content)
                    SELECT %s, user_id, username, %s
                    FROM users_secrets
                    JOIN users ON users_secrets.user_id = users.id
                    WHERE secret = %s
                """, (post_id, content, jwt))

            cursor.execute("COMMIT")
            return {"success": "Успех"}
    except Exception as e:
        cursor.execute("ROLLBACK")
    finally:
        release_connection(conn)


def check_valid_jwt_key(secret, tg_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users_secrets WHERE secret = %s", (secret,))
            data = cursor.fetchall()
            if data:
                cursor.execute(f"UPDATE users_secrets SET telegram_id = %s WHERE user_id = %s", (tg_id, data[0][0]))
                cursor.execute("COMMIT")
                return checks['success']
            return checks['denied']
    finally:
        release_connection(conn)


def take_posts_api(jwt):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users_secrets WHERE secret = %s", (jwt,))
            data = cursor.fetchall()
            if data:
                cursor.execute(f"SELECT * FROM posts ORDER BY id ")
                return cursor.fetchall()
    finally:
        release_connection(conn)

def take_one_post_api(id):
    result = {}
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts WHERE id = %s", (id,))
            data = cursor.fetchall()
            result['post_data'] = data
            cursor.execute(f"SELECT * FROM comments WHERE post_id = %s", (id,))
            data = cursor.fetchall()
            result['comment'] = data
            return result
    finally:
        release_connection(conn)


