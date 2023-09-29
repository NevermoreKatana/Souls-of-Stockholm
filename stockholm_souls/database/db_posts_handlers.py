from stockholm_souls.database.db_conn import release_connection, get_connection


def take_one_post(id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)


def take_comments(post_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
            data = cursor.fetchall()
            return data
    finally:
        release_connection(conn)


def add_comments(post_id, content, user_data):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO comments (post_id, user_id, username, content) VALUES (%s, %s, %s, %s)", (post_id, user_data['id'], user_data['name'], content,))
            cursor.execute("COMMIT")
    finally:
        release_connection(conn)


def add_new_post(user_id, username, post_name, content):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO posts (user_id, user_name, name, content) VALUES (%s,%s,%s,%s)", (user_id, username, post_name, content))
            cursor.execute("COMMIT")
    finally:
        release_connection(conn)


def take_all_posts():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts ORDER BY id")
            info = cursor.fetchall()
            return info
    finally:
        release_connection(conn)
