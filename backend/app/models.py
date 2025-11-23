# app/models.py
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class Hack(BaseModel):
    id: Optional[str] = None
    source: Optional[str] = None
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    url: Optional[HttpUrl] = None
    categories: List[str] = []
    tags: List[str] = []
    image_url: Optional[HttpUrl] = None
    excerpt: Optional[str] = None
    score: Optional[float] = None

class SearchResult(BaseModel):
    total: int          
    page: int            
    page_size: int      
    total_pages: int     
    hits: List[Hack]
