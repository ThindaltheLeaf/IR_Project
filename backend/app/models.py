# app/models.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Hack(BaseModel):
    id: str                      # Mongo _id as string
    source: Optional[str] = None # which site / spider
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None   # could be refined later to datetime
    url: Optional[HttpUrl] = None
    categories: List[str] = []
    tags: List[str] = []
    image_url: Optional[HttpUrl] = None
    excerpt: Optional[str] = None

class SearchResult(BaseModel):
    total: int
    hits: List[Hack]
