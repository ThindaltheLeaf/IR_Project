from bson import ObjectId
from typing import Any, Dict
from app.models import Hack

def mongo_doc_to_hack(doc: Dict[str, Any]) -> Hack:
    return Hack(
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
