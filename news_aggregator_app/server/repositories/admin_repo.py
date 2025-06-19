from server.db.db import get_db_connection

def list_sources_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM external_sources")
    sources = cursor.fetchall()
    cursor.close()
    conn.close()
    return sources

def get_source_db(source_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM external_sources WHERE id=%s", (source_id,))
    source = cursor.fetchone()
    cursor.close()
    conn.close()
    return source

def update_source_db(source_id, api_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE external_sources SET api_key=%s WHERE id=%s", (api_key, source_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Source updated."}

def add_source_db(name, api_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO external_sources (name, api_key) VALUES (%s, %s)", (name, api_key))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Source added."}

def add_category_db(name, description=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Category added."}