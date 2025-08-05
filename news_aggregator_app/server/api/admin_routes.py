from fastapi import APIRouter, HTTPException
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
    get_article_report_details_controller,
    get_hidden_articles_controller,
)
from server.schemas.admin_schema import UpdateSourceRequest, AddSourceRequest, AddCategoryRequest, FilteredKeywordRequest

router = APIRouter()

@router.get("/external-sources")
def sources():
    return list_sources()

@router.get("/external-sources/{source_id}")
def source(source_id: int):
    return get_source(source_id)

@router.put("/external-sources/{source_id}")
def update(source_id: int, request: UpdateSourceRequest):
    return update_source(source_id, request.api_key)

@router.post("/external-sources")
def add(request: AddSourceRequest):
    return add_source(request.name, request.api_key)

@router.post("/categories")
def add_cat(request: AddCategoryRequest):
    return add_category(request.name, request.description)

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
def add_keyword(request: FilteredKeywordRequest):
    return add_filtered_keyword_controller(request.keyword)

@router.delete("/filtered-keywords")
def remove_keyword(request: FilteredKeywordRequest):
    return remove_filtered_keyword_controller(request.keyword)

@router.get("/filtered-keywords")
def list_keywords():
    return get_filtered_keywords_controller()

@router.get("/reported-articles/{article_id}/details")
def article_report_details(article_id: int):
    return get_article_report_details_controller(article_id)

@router.post("/articles/{article_id}/toggle-visibility")
def toggle_article_visibility(article_id: int, hide: bool):
    return hide_article(article_id, hide)

@router.get("/hidden-articles")
def hidden_articles():
    return get_hidden_articles_controller()
