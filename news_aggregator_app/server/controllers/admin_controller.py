from server.repositories.admin_repo import (
    list_sources_db, get_source_db, update_source_db, add_source_db, add_category_db
)

def list_sources():
    return list_sources_db()

def get_source(source_id):
    return get_source_db(source_id)

def update_source(source_id, api_key):
    return update_source_db(source_id, api_key)

def add_source(name, api_key):
    return add_source_db(name, api_key)

def add_category(name, description=None):
    return add_category_db(name, description)