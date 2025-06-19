from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    content: Optional[str]
    url: str
    source: str
    category: str
    published_at: datetime

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True