import mysql.connector
from server.config import DB_CONFIG

def get_db_connection():
    config = DB_CONFIG.copy()
    config['autocommit'] = True
    return mysql.connector.connect(**config)