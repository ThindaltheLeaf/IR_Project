# app/routers/hacks.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from bson import ObjectId

from app.services.mongo import get_collection
from app.models import Hack
from app.utils import mongo_doc_to_hack

router = APIRouter(prefix="/api/hacks", tags=["hacks"])

# Helper: all collections used by the Scrapy pipeline
COLLECTIONS = [
    "hacks_ikea",
    "hacks_love_property",
    "hacks_tosize",
    "hacks_reddit",
]

def iter_all_collections():
    for name in COLLECTIONS:
        yield get_collection(name)

@router.get("/", response_model=List[Hack])
def list_hacks(
    source: Optional[str] = Query(
        None,
        description="Filter by source (ikea, love_property, tosize, reddit)",
    ),
    limit: int = 20,
):
    """
    List hacks from MongoDB.
    - If `source` is given, only from that spider/website.
    - Otherwise, merge all collections (simple for now).
    """
    docs = []

    if source:
        col_name = f"hacks_{source}"
        col = get_collection(col_name)
        docs = list(col.find().limit(limit))
    else:
        # naive merge from all collections
        remaining = limit
        for col in iter_all_collections():
            if remaining <= 0:
                break
            chunk = list(col.find().limit(remaining))
            docs.extend(chunk)
            remaining -= len(chunk)

    return [mongo_doc_to_hack(d) for d in docs]


@router.get("/{hack_id}", response_model=Hack)
def get_hack(hack_id: str):
    """
    Fetch a single hack by Mongo _id (string) across all collections.
    """
    _id = ObjectId(hack_id)

    for col in iter_all_collections():
        doc = col.find_one({"_id": _id})
        if doc:
            return mongo_doc_to_hack(doc)

    raise HTTPException(status_code=404, detail="Hack not found")
