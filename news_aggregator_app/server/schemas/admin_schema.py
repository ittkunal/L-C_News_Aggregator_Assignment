from pydantic import BaseModel, validator
from typing import Optional

class UpdateSourceRequest(BaseModel):
    api_key: str
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or not v.strip():
            raise ValueError('API key cannot be empty or blank')
        return v.strip()

class AddSourceRequest(BaseModel):
    name: str
    api_key: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Source name cannot be empty or blank')
        return v.strip()
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or not v.strip():
            raise ValueError('API key cannot be empty or blank')
        return v.strip()

class AddCategoryRequest(BaseModel):
    name: str
    description: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Category name cannot be empty or blank')
        return v.strip()

class FilteredKeywordRequest(BaseModel):
    keyword: str
    
    @validator('keyword')
    def validate_keyword(cls, v):
        if not v or not v.strip():
            raise ValueError('Keyword cannot be empty or blank')
        return v.strip() 