from fastapi import APIRouter
from app.services.mongo import get_db

router = APIRouter(prefix="/api/debug", tags=["debug"])

@router.get("/collections")
def list_collections():
    db = get_db()
    return {"collections": db.list_collection_names()}


@router.get("/ping")
def ping_db():
    db = get_db()
    try:
        db.command("ping")
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}