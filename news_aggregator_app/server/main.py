from fastapi import FastAPI
from server.api import auth_routes, news_routes, admin_routes, user_routes
from server.jobs.scheduler import start_scheduler  # needs a stop_scheduler function ideally
from server.services.news_fetcher import fetch_and_store_news

app = FastAPI(title="News Aggregator API")

# Include your API routers with proper tags and prefixes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(news_routes.router, prefix="/news", tags=["news"])
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(user_routes.router, prefix="/user", tags=["user"])

@app.on_event("startup")
async def on_startup():
    # Start the scheduler to run periodic jobs (like news fetching)
    start_scheduler()
    # Optionally run the first news fetch immediately on startup
    fetch_and_store_news()
