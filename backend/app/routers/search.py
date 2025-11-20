# app/routers/search.py
from fastapi import APIRouter, Query
from typing import Optional
from app.models import SearchResult, Hack

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/", response_model=SearchResult)
def search(
    q: Optional[str] = Query("", description="Search query (will use Solr later)"),
    page: int = 1,
    page_size: int = 10,
):
    # temporary dummy implementation
    dummy = Hack(
        id="dummy",
        source="dummy",
        title=f"Example result for '{q}'",
        content="Search will be powered by Solr later.",
        author=None,
        date=None,
        url=None,
        categories=[],
        tags=[],
        image_url=None,
        excerpt=None,
    )
    return SearchResult(total=1, hits=[dummy])
