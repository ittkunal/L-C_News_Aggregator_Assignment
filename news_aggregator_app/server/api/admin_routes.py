from fastapi import APIRouter
from server.controllers.admin_controller import (
    list_sources,
    get_source,
    update_source,
    add_source,
    add_category,
    get_reported_articles,
    hide_article,
    hide_category,
    add_filtered_keyword_controller,
    remove_filtered_keyword_controller,
    get_filtered_keywords_controller,
)

router = APIRouter()

@router.get("/external-sources")
def sources():
    return list_sources()

@router.get("/external-sources/{source_id}")
def source(source_id: int):
    return get_source(source_id)

@router.put("/external-sources/{source_id}")
def update(source_id: int, api_key: str):
    return update_source(source_id, api_key)

@router.post("/external-sources")
def add(name: str, api_key: str):
    return add_source(name, api_key)

@router.post("/categories")
def add_cat(name: str, description: str = None):
    return add_category(name, description)

@router.get("/reported-articles")
def reported_articles():
    return get_reported_articles()

@router.post("/hide-article")
def hide_article_route(article_id: int, hide: bool):
    return hide_article(article_id, hide)

@router.post("/hide-category")
def hide_category_route(category: str, hide: bool):
    return hide_category(category, hide)

@router.post("/filtered-keywords")
def add_keyword(keyword: str):
    return add_filtered_keyword_controller(keyword)

@router.delete("/filtered-keywords")
def remove_keyword(keyword: str):
    return remove_filtered_keyword_controller(keyword)

@router.get("/filtered-keywords")
def list_keywords():
    return get_filtered_keywords_controller()

# Optional: Uncomment and add if you have category update in your admin_repo.py
# @router.put("/categories/{category_id}")
# def update_category(category_id: int, name: str = None, description: str = None):
#     from server.repositories.admin_repo import update_category_db
#     return update_category_db(category_id, name, description)
