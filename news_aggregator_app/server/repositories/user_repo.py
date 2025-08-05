from server.db.db import get_db_connection
from server.repositories.article_repo import article_exists

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_user(username, email, password_hash, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
        (username, email, password_hash, is_admin)
    )
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user(user_id, username=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if username and email:
        cursor.execute("UPDATE users SET username=%s, email=%s WHERE id=%s", (username, email, user_id))
    elif username:
        cursor.execute("UPDATE users SET username=%s WHERE id=%s", (username, user_id))
    elif email:
        cursor.execute("UPDATE users SET email=%s WHERE id=%s", (email, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Profile updated."}

def get_saved_articles_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.* FROM saved_articles sa
        JOIN articles a ON sa.article_id = a.id
        WHERE sa.user_id=%s AND a.hidden=0
        ORDER BY sa.saved_at DESC
    """, (user_id,))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def save_article_db(user_id, article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First check if the article exists and is not hidden
    if not article_exists(article_id):
        cursor.close()
        conn.close()
        return {"error": "Article not found"}
    
    # Check if already saved
    cursor.execute("SELECT id FROM saved_articles WHERE user_id=%s AND article_id=%s", (user_id, article_id))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {"error": "Article already saved"}
    
    # Save the article
    cursor.execute("INSERT INTO saved_articles (user_id, article_id) VALUES (%s, %s)", (user_id, article_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Article saved."}

def delete_saved_article_db(user_id, article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the saved article exists
    cursor.execute("SELECT id FROM saved_articles WHERE user_id=%s AND article_id=%s", (user_id, article_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return {"error": "Saved article not found"}
    
    cursor.execute("DELETE FROM saved_articles WHERE user_id=%s AND article_id=%s", (user_id, article_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Article deleted from saved list."}

def get_notifications_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE user_id=%s", (user_id,))
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return notifications

def update_notifications_db(user_id, keywords=None, enabled=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if keywords is not None and enabled is not None:
        cursor.execute("UPDATE notifications SET keywords=%s, enabled=%s WHERE user_id=%s", (keywords, enabled, user_id))
    elif keywords is not None:
        cursor.execute("UPDATE notifications SET keywords=%s WHERE user_id=%s", (keywords, user_id))
    elif enabled is not None:
        cursor.execute("UPDATE notifications SET enabled=%s WHERE user_id=%s", (enabled, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Notification settings updated."}

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users