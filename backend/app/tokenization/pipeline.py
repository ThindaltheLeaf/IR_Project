# app/tokenization/pipeline.py
from typing import Optional, Dict, Any
import urllib.parse

from bson import ObjectId

from app.models import Hack
from app.services.mongo import get_collection

from app.tokenization.config import HACKS_COLLECTION_NAME
from app.tokenization.llm_local import tag_hack_with_llm


def _iter_hacks_needing_tokens(limit: Optional[int] = None):
    """
    Yield Mongo docs that don't have tags/categories yet.
    Adjust the filter if you want to re-tag everything.
    """
    coll = get_collection(HACKS_COLLECTION_NAME)

    query: Dict[str, Any] = {
        "$or": [
            {"tags": {"$exists": False}},
            {"tags": {"$size": 0}},
            {"categories": {"$exists": False}},
            {"categories": {"$size": 0}},
        ]
    }

    cursor = coll.find(query)
    if limit is not None:
        cursor = cursor.limit(limit)

    for doc in cursor:
        # Normalize relative image URLs so Pydantic accepts them as valid URLs
        image = doc.get("image_url")
        if isinstance(image, str) and image.startswith("/"):
            doc["image_url"] = urllib.parse.urljoin(
                "https://www.reddit.com", image)

        yield doc


def run_tokenization(limit: Optional[int] = None) -> None:
    """
    For each Hack document that needs tokens:
      - build Hack model
      - call LLM
      - update Mongo with categories+tags
    """
    coll = get_collection(HACKS_COLLECTION_NAME)

    processed = 0
    for doc in _iter_hacks_needing_tokens(limit=limit):
        hack = Hack(
            id=str(doc["_id"]),
            source=doc.get("source"),
            title=doc.get("title", ""),
            content=doc.get("content"),
            author=doc.get("author"),
            date=doc.get("date"),
            url=doc.get("url"),
            categories=doc.get("categories") or [],
            tags=doc.get("tags") or [],
            image_url=doc.get("image_url"),
            excerpt=doc.get("excerpt"),
        )

        categories, tags = tag_hack_with_llm(hack)

        if not categories and not tags:
            print(f"[SKIP] No tokens generated for {hack.id} ({hack.title})")
            continue

        coll.update_one(
            {"_id": ObjectId(hack.id)},
            {"$set": {"categories": categories, "tags": tags}},
        )
        processed += 1
        print(
            f"[OK] {hack.id} | {hack.title[:60]!r} → {categories} | {len(tags)} tags")

    print(f"Done. Updated {processed} hacks.")
