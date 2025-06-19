from fastapi import APIRouter
from server.controllers.admin_controller import (
    list_sources, get_source, update_source, add_source, add_category
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