from fastapi import APIRouter, Depends, Query
from typing import List

from app.models import Hack, SearchResult
from app.services import mongo

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/", response_model=SearchResult)
def search_hacks(
    query: str = Query(..., description="Search term"),
    limit: int = Query(10, ge=1, le=50),
    db = Depends(mongo.get_db),
):
    """
    Search API to query the hacks_all collection using MongoDB Atlas Search.
    """
    index_name = mongo.MONGO_SEARCH_INDEX 
    pipeline = [
        {
            "$search": {
                "index": index_name,
                "text": {
                    "query": query,
                    "path": {
                        "wildcard": "*"  
                    }
                }
            }
        },
        {
            "$limit": limit
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
        }
    ]

    docs = list(db["hacks_all"].aggregate(pipeline))
    hits: List[Hack] = [Hack(**doc) for doc in docs]
   
    return SearchResult(total=len(hits), hits=hits)
