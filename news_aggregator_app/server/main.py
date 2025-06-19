from fastapi import FastAPI
from server.api import auth_routes, news_routes, admin_routes, user_routes
from server.jobs.scheduler import start_scheduler
from server.services.news_fetcher import fetch_and_store_news

app = FastAPI(title="News Aggregator API")

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(news_routes.router, prefix="/news", tags=["news"])
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(user_routes.router, prefix="/user", tags=["user"])

start_scheduler()
fetch_and_store_news()