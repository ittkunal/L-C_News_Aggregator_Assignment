import mysql.connector
from server.config import DB_CONFIG

def migrate_database():
    """Add missing columns to existing tables."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Check if reason column exists in article_reports table
        cursor.execute("SHOW COLUMNS FROM article_reports LIKE 'reason'")
        if not cursor.fetchone():
            print("Adding 'reason' column to article_reports table...")
            cursor.execute("ALTER TABLE article_reports ADD COLUMN reason VARCHAR(255)")
            print("✅ 'reason' column added successfully!")
        else:
            print("✅ 'reason' column already exists in article_reports table")
        
        # Check if hidden column exists in articles table
        cursor.execute("SHOW COLUMNS FROM articles LIKE 'hidden'")
        if not cursor.fetchone():
            print("Adding 'hidden' column to articles table...")
            cursor.execute("ALTER TABLE articles ADD COLUMN hidden BOOLEAN DEFAULT FALSE")
            print("✅ 'hidden' column added successfully!")
        else:
            print("✅ 'hidden' column already exists in articles table")
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate_database() 