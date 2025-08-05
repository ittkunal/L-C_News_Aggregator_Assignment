import mysql.connector
from server.config import DB_CONFIG

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        description TEXT,
        hidden BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # External Sources Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS external_sources (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        api_key VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Articles Table with existing 'category' column (string) and new is_hidden
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        url VARCHAR(255) NOT NULL,
        source VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL DEFAULT 'general',
        published_at DATETIME NOT NULL,
        is_hidden BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Saved Articles Table
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

    # Notifications Table (user settings)
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

    # Sessions Table for user sessions/tokens
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

    # Likes/Dislikes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes_dislikes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        article_id INT NOT NULL,
        like_dislike INT NOT NULL,  -- 1 for like, -1 for dislike
        UNIQUE KEY user_article_like_uc (user_id, article_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
    )
    """)

    # Article Reports Table - for user reports on articles (Complexity 1 feature)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article_reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        article_id INT NOT NULL,
        user_id INT NOT NULL,
        reason VARCHAR(255),
        reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY user_article_report_uc (user_id, article_id),
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Filtered Keywords Table for admin-blocked keywords
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filtered_keywords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        keyword VARCHAR(100) UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Migration: Add missing columns if they don't exist
    try:
        # Check if reason column exists in article_reports table
        cursor.execute("SHOW COLUMNS FROM article_reports LIKE 'reason'")
        if not cursor.fetchone():
            print("Adding 'reason' column to article_reports table...")
            cursor.execute("ALTER TABLE article_reports ADD COLUMN reason VARCHAR(255)")
            print("✅ 'reason' column added successfully!")
        
        # Check if hidden column exists in articles table
        cursor.execute("SHOW COLUMNS FROM articles LIKE 'hidden'")
        if not cursor.fetchone():
            print("Adding 'hidden' column to articles table...")
            cursor.execute("ALTER TABLE articles ADD COLUMN hidden BOOLEAN DEFAULT FALSE")
            print("✅ 'hidden' column added successfully!")
    except Exception as e:
        print(f"Migration warning: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized with updated schema (no renaming).")

if __name__ == "__main__":
    init_db()
