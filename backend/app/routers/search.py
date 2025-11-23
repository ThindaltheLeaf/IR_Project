from fastapi import APIRouter, Depends, Query
from typing import List
import math

from app.models import Hack, SearchResult
from app.services import mongo

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/", response_model=SearchResult)
def search_hacks(
    query: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db = Depends(mongo.get_db),
):
    """
    Search API to query the hacks_all collection using MongoDB Atlas Search.
    - Uses $search for ranked hits
    - Uses $searchMeta for true total count
    """
    index_name = mongo.MONGO_SEARCH_INDEX
    collection = db["hacks_all"]

    # ---------- 1) $search for the current page of hits ----------
    skip = (page - 1) * page_size

    search_pipeline = [
        {
            "$search": {
                "index": index_name,
                "text": {
                    "query": query,
                    "path": {
                        "wildcard": "*"
                    },
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "id": {"$toString": "$_id"},
                "source": 1,
                "url": 1,
                "author": 1,
                "categories": 1,
                "content": 1,
                "date": 1,
                "excerpt": 1,
                "image_url": 1,
                "tags": 1,
                "title": 1,
                "score": {"$meta": "searchScore"},
            }
        },
        {"$skip": skip},
        {"$limit": page_size},
    ]

    hit_docs = list(collection.aggregate(search_pipeline))
    hits: List[Hack] = [Hack(**doc) for doc in hit_docs]

    # ---------- 2) $searchMeta to get true total matches ----------
    count_pipeline = [
        {
            "$searchMeta": {
                "index": index_name,
                "text": {
                    "query": query,
                    "path": {
                        "wildcard": "*"
                    },
                },
                "count": {
                    "type": "total",
                },
            }
        }
    ]

    meta_docs = list(collection.aggregate(count_pipeline))
    if meta_docs and "count" in meta_docs[0]:
        total = meta_docs[0]["count"]["total"]
    else:
        total = 0

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return SearchResult(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        hits=hits,
    )
