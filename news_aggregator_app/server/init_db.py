from server.db.db import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(128) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        url VARCHAR(255) NOT NULL,
        source VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL DEFAULT 'general',
        published_at DATETIME NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS external_sources (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        api_key VARCHAR(255) NOT NULL,
        status BOOLEAN DEFAULT TRUE,
        last_accessed DATETIME
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        article_id INT NOT NULL,
        saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY user_article_uc (user_id, article_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        type VARCHAR(50) NOT NULL,
        keywords TEXT,
        enabled BOOLEAN DEFAULT TRUE,
        last_sent DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        session_token VARCHAR(255) UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        description VARCHAR(255)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes_dislikes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        article_id INT NOT NULL,
        like_dislike INT NOT NULL,
        UNIQUE KEY user_article_like_uc (user_id, article_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()