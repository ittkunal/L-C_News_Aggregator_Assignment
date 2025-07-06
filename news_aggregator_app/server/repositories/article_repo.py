from server.db.db import get_db_connection
from datetime import datetime, timedelta

def store_articles(articles):
    conn = get_db_connection()
    cursor = conn.cursor()
    stored_count = 0
    for art in articles:
        print(f"[DB] Attempting to store: {art['title']} | {art['url']}")
        try:
            cursor.execute("SELECT id FROM articles WHERE url=%s", (art["url"],))
            if not cursor.fetchone():
                published_at = art["published_at"]
                if published_at:
                    try:
                        published_at = published_at.replace("Z", "+00:00")
                        published_at = datetime.fromisoformat(published_at)
                    except Exception as e:
                        print(f"[DB] Date parse error for '{art['title']}': {published_at} | {e}")
                        published_at = None
                cursor.execute(
                    "INSERT INTO articles (title, content, url, source, category, published_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        art["title"],
                        art["content"],
                        art["url"],
                        art["source"],
                        art["category"],
                        published_at
                    )
                )
                stored_count += 1
            else:
                print(f"[DB] Article already exists: {art['url']}")
        except Exception as e:
            print(f"[DB] Error storing article '{art['title']}': {e}")
    conn.commit()
    print(f"[DB] Stored {stored_count} new articles.")
    cursor.close()
    conn.close()

def get_articles(date=None, start=None, end=None, category=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM articles WHERE hidden=0"
    params = []
    if category:
        query += " AND category=%s"
        params.append(category)
    if date:
        query += " AND DATE(published_at)=%s"
        params.append(date)
    if start and end:
        query += " AND DATE(published_at) BETWEEN %s AND %s"
        params.extend([start, end])
    hidden_cats = get_hidden_categories()
    if hidden_cats:
        query += " AND category NOT IN (%s)" % (",".join(["%s"]*len(hidden_cats)))
        params.extend(hidden_cats)
    filtered = get_filtered_keywords()
    if filtered:
        for kw in filtered:
            query += " AND title NOT LIKE %s AND content NOT LIKE %s"
            params.extend([f"%{kw}%", f"%{kw}%"])
    query += " ORDER BY published_at DESC"
    cursor.execute(query, tuple(params))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def get_article_by_id(article_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles WHERE id=%s", (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    return article

def search_articles_db(q, start=None, end=None, sort_by=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT a.*, COALESCE(SUM(ld.like_dislike),0) as score FROM articles a LEFT JOIN likes_dislikes ld ON a.id=ld.article_id WHERE (a.title LIKE %s OR a.content LIKE %s)"
    params = [f"%{q}%", f"%{q}%"]
    if start and end:
        query += " AND DATE(a.published_at) BETWEEN %s AND %s"
        params.extend([start, end])
    query += " GROUP BY a.id"
    if sort_by == "likes":
        query += " ORDER BY score DESC"
    elif sort_by == "dislikes":
        query += " ORDER BY score ASC"
    else:
        query += " ORDER BY a.published_at DESC"
    cursor.execute(query, tuple(params))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def get_categories_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

def like_article_db(article_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO likes_dislikes (user_id, article_id, like_dislike) VALUES (%s, %s, 1)", (user_id, article_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Article liked."}

def dislike_article_db(article_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO likes_dislikes (user_id, article_id, like_dislike) VALUES (%s, %s, -1)", (user_id, article_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Article disliked."}

def get_recent_articles(hours=3):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM articles WHERE published_at >= %s", (since,))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def report_article_db(article_id, user_id, threshold=3):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM article_reports WHERE article_id=%s AND user_id=%s", (article_id, user_id))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO article_reports (article_id, user_id) VALUES (%s, %s)", (article_id, user_id))
        conn.commit()
    cursor.execute("SELECT COUNT(*) as cnt FROM article_reports WHERE article_id=%s", (article_id,))
    count = cursor.fetchone()[0]
    if count >= threshold:
        cursor.execute("UPDATE articles SET hidden=1 WHERE id=%s", (article_id,))
        conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Article reported. Total reports: {count}"}

def count_reports(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM article_reports WHERE article_id=%s", (article_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def set_article_hidden(article_id, hide):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE articles SET hidden=%s WHERE id=%s", (1 if hide else 0, article_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Article {'hidden' if hide else 'unhidden'}."}

def get_reported_articles_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, COUNT(r.id) as report_count
        FROM articles a
        JOIN article_reports r ON a.id = r.article_id
        GROUP BY a.id
        ORDER BY report_count DESC
    """)
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return articles

def set_category_hidden(category, hide):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET hidden=%s WHERE name=%s", (1 if hide else 0, category))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Category '{category}' {'hidden' if hide else 'unhidden'}."}

def get_hidden_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories WHERE hidden=1")
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categories

def get_filtered_keywords():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM filtered_keywords")
    keywords = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return keywords

def add_filtered_keyword(keyword):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO filtered_keywords (keyword) VALUES (%s)", (keyword,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Keyword added."}

def remove_filtered_keyword(keyword):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filtered_keywords WHERE keyword=%s", (keyword,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Keyword removed."}