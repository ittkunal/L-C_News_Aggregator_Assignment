from apscheduler.schedulers.background import BackgroundScheduler
from server.services.news_fetcher import fetch_and_store_news
from server.services.notifier import send_batch_notifications

def scheduled_job():
    fetch_and_store_news()
    send_batch_notifications()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', hours=3)
    scheduler.start()