import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Enolahomes@12")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "news_aggregator")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    THENEWSAPI_KEY = os.getenv("THENEWSAPI_KEY")

print("DB_USER:", Config.DB_USER)
print("DB_PASSWORD:", Config.DB_PASSWORD)
print("DB_HOST:", Config.DB_HOST)
print("DB_NAME:", Config.DB_NAME)