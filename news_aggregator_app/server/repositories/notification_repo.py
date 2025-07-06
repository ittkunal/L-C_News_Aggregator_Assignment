from server.db.db import get_db_connection

def get_notifications_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE user_id=%s", (user_id,))
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return notifications

def update_notification(user_id, category, enabled=None, keywords=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM notifications WHERE user_id=%s AND type=%s", (user_id, category))
    row = cursor.fetchone()
    if row:
        if enabled is not None and keywords is not None:
            cursor.execute(
                "UPDATE notifications SET enabled=%s, keywords=%s WHERE user_id=%s AND type=%s",
                (enabled, keywords, user_id, category)
            )
        elif enabled is not None:
            cursor.execute(
                "UPDATE notifications SET enabled=%s WHERE user_id=%s AND type=%s",
                (enabled, user_id, category)
            )
        elif keywords is not None:
            cursor.execute(
                "UPDATE notifications SET keywords=%s WHERE user_id=%s AND type=%s",
                (keywords, user_id, category)
            )
    else:
        cursor.execute(
            "INSERT INTO notifications (user_id, type, enabled, keywords) VALUES (%s, %s, %s, %s)",
            (user_id, category, enabled if enabled is not None else 0, keywords if keywords is not None else "")
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Notification settings updated."}

def get_users_for_notification():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT u.email, n.type, n.keywords FROM users u JOIN notifications n ON u.id = n.user_id WHERE n.enabled=1")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users