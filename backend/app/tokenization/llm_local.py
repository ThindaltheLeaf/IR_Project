# app/tokenization/llm_local.py
import json
import requests
from typing import List, Tuple, Optional

from app.models import Hack
from app.tokenization.config import IKEA_HACKS_CATEGORIES

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"

# Improved system prompt with examples and clearer instructions
SYSTEM_PROMPT = f"""
You are an expert assistant that tags IKEA hack posts with categories and descriptive tags.

CATEGORIES (choose 1-3 that best match):
{", ".join(IKEA_HACKS_CATEGORIES)}

TAGGING GUIDELINES:
1. Include specific IKEA product names in UPPERCASE (KALLAX, BILLY, LACK, MALM, etc.)
2. Add descriptive attributes (painted, wall-mounted, with wheels, added legs, custom top)
3. Include functional tags (shoe storage, kids room, home office, plant stand)
4. Use materials when relevant (wood, metal, fabric, glass)
5. Keep tags concise (2-4 words max)
6. Generate 4-6 relevant tags
7. AVOID generic tags like "IKEA", "IKEA Hack", "DIY" - be specific!
8. Choose maximum 3 categories, prioritize the most specific ones

EXAMPLES:

Example 1:
Post: {{"title": "KALLAX Bench with Storage", "content": "I turned a KALLAX shelf on its side and added cushions on top to create a window seat with storage underneath. Perfect for the entryway!"}}
Output: {{"categories": ["Entryway", "Seating", "Secondary Storage"], "tags": ["KALLAX", "bench", "window seat", "cushioned top", "shoe storage", "entryway seating"]}}

Example 2:
Post: {{"title": "LACK Side Table Plant Stand", "content": "Stacked three LACK tables and painted them gold. Now it's a multi-level plant stand for my succulents."}}
Output: {{"categories": ["Outdoor", "IKEA Living Room Hacks"], "tags": ["LACK", "plant stand", "stacked tables", "gold painted", "succulents", "multi-level"]}}

Example 3:
Post: {{"title": "BILLY Bookcase Built-in", "content": "Added crown molding and a custom base to BILLY bookcases to make them look like expensive built-ins. Painted white to match the room."}}
Output: {{"categories": ["IKEA Bookshelf Hacks", "IKEA Living Room Hacks"], "tags": ["BILLY", "built-in look", "crown molding", "painted white", "custom base"]}}

Now tag the following post. Output ONLY valid JSON, no markdown, no explanation:
"""


def _build_user_prompt(hack: Hack) -> str:
    """Build a concise user prompt with all available information."""
    content = (hack.content or hack.excerpt or "")[:800]

    # Include image URL info if available - visual context helps
    has_image = " (includes image)" if hack.image_url else ""

    return f"""
Post{has_image}:
{{
  "title": {json.dumps(hack.title)},
  "content": {json.dumps(content)}
}}

Remember: Output ONLY the JSON object with "categories" and "tags" arrays.
"""


def _clean_llm_response(text: str) -> str:
    """Clean common LLM output formatting issues."""
    text = text.strip()

    # Remove markdown code blocks
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    # Remove any text before first { or after last }
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    return text


def _validate_and_clean_tags(
    raw_categories: List[str],
    raw_tags: List[str]
) -> Tuple[List[str], List[str]]:
    """Validate categories against allowed list and deduplicate tags."""

    # Validate categories - limit to top 2
    categories = [
        c for c in raw_categories
        if isinstance(c, str) and c in IKEA_HACKS_CATEGORIES
    ][:3]  # Keep max 3 categories

    # Generic tags to skip
    SKIP_TAGS = {'ikea', 'ikea hack', 'ikea hacks', 'diy', 'hack'}

    # Clean and deduplicate tags
    tags: List[str] = []
    seen = set()

    for t in raw_tags:
        if not isinstance(t, str):
            continue

        t_clean = t.strip()
        if not t_clean or len(t_clean) > 50:  # Skip overly long tags
            continue

        # Skip generic tags
        if t_clean.lower() in SKIP_TAGS:
            continue

        # Case-insensitive deduplication
        key = t_clean.lower()
        if key in seen:
            continue

        seen.add(key)
        tags.append(t_clean)

    return categories, tags


def tag_hack_with_llm(
    hack: Hack,
    timeout: int = 120,
    retry_on_failure: bool = True
) -> Tuple[List[str], List[str]]:
    """
    Tag a hack using local LLM via Ollama.

    Args:
        hack: The Hack object to tag
        timeout: Request timeout in seconds
        retry_on_failure: Whether to retry once on failure

    Returns:
        Tuple of (categories, tags)
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(hack)},
    ]

    attempt = 0
    max_attempts = 2 if retry_on_failure else 1

    while attempt < max_attempts:
        attempt += 1

        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Lower temperature for more consistent output
                        "top_p": 0.9,
                    }
                },
                timeout=timeout,
            )
            r.raise_for_status()
        except requests.exceptions.Timeout:
            print(
                f"[LLM ERROR] Timeout for {hack.title!r} (attempt {attempt}/{max_attempts})")
            if attempt < max_attempts:
                continue
            return [], []
        except Exception as e:
            print(f"[LLM ERROR] Request failed for {hack.title!r}: {e}")
            if attempt < max_attempts:
                continue
            return [], []

        data = r.json()
        text = data.get("message", {}).get("content", "").strip()

        if not text:
            print(f"[LLM ERROR] Empty response for {hack.title!r}")
            if attempt < max_attempts:
                continue
            return [], []

        # Clean the response
        text = _clean_llm_response(text)

        # Parse JSON
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"[LLM ERROR] JSON parse failed for {hack.title!r}: {e}")
            print(f"Raw response: {text[:400]}")
            if attempt < max_attempts:
                continue
            return [], []

        # Extract and validate
        raw_categories = parsed.get("categories") or []
        raw_tags = parsed.get("tags") or []

        if not isinstance(raw_categories, list) or not isinstance(raw_tags, list):
            print(f"[LLM ERROR] Invalid response structure for {hack.title!r}")
            if attempt < max_attempts:
                continue
            return [], []

        categories, tags = _validate_and_clean_tags(raw_categories, raw_tags)

        # Success - return results
        if categories or tags:
            return categories, tags

        # If we got valid JSON but no useful tags, retry
        print(
            f"[LLM WARNING] No valid categories/tags for {hack.title!r} (attempt {attempt}/{max_attempts})")
        if attempt < max_attempts:
            continue

    return [], []


def tag_hack_with_fallback(hack: Hack) -> Tuple[List[str], List[str]]:
    """
    Tag a hack with LLM, falling back to rule-based tagging if LLM fails.
    """
    categories, tags = tag_hack_with_llm(hack)

    if not categories and not tags:
        # Fallback: extract IKEA product names from title/content
        text = f"{hack.title} {hack.content or hack.excerpt or ''}".upper()

        common_products = [
            "KALLAX", "BILLY", "LACK", "MALM", "HEMNES", "BESTA",
            "PAX", "IVAR", "EKET", "FJALLBO", "TARVA", "RAST",
            "VITTSJO", "BRIMNES", "ALEX", "MICKE", "LISABO"
        ]

        fallback_tags = [p for p in common_products if p in text]

        if fallback_tags:
            return [], fallback_tags

    return categories, tags


# Improved pipeline.py functions
def run_tokenization_batch(
    limit: Optional[int] = None,
    batch_size: int = 10,
    skip_existing: bool = False
) -> None:
    """
    Process hacks in batches with progress tracking and better error handling.

    Args:
        limit: Maximum number of hacks to process
        batch_size: Number of hacks to process before committing
        skip_existing: If True, skip hacks that already have categories/tags
    """
    from bson import ObjectId
    from app.services.mongo import get_collection
    from app.tokenization.config import HACKS_COLLECTION_NAME

    coll = get_collection(HACKS_COLLECTION_NAME)

    # Build query
    query = {}
    if skip_existing:
        query = {
            "$or": [
                {"categories": {"$exists": False}},
                {"categories": []},
                {"tags": {"$exists": False}},
                {"tags": []}
            ]
        }

    cursor = coll.find(query)
    if limit is not None:
        cursor = cursor.limit(limit)

    total = coll.count_documents(query)
    print(
        f"Processing {total if limit is None else min(total, limit)} hacks...")

    processed = 0
    successful = 0
    failed = 0
    batch = []

    for doc in cursor:
        # Fix image URLs
        image = doc.get("image_url")
        if isinstance(image, str) and image.startswith("/"):
            doc["image_url"] = f"https://www.reddit.com{image}"

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

        categories, tags = tag_hack_with_fallback(hack)

        if not categories and not tags:
            print(f"[SKIP] No tokens for {hack.id} | {hack.title[:50]}")
            failed += 1
            processed += 1
            continue

        batch.append({
            "id": hack.id,
            "categories": categories,
            "tags": tags,
            "title": hack.title
        })

        # Commit batch
        if len(batch) >= batch_size:
            _commit_batch(coll, batch)
            successful += len(batch)
            processed += len(batch)
            print(
                f"Progress: {processed}/{total} ({successful} successful, {failed} failed)")
            batch = []

    # Commit remaining
    if batch:
        _commit_batch(coll, batch)
        successful += len(batch)
        processed += len(batch)

    print(
        f"\n✓ Done! Processed {processed} hacks ({successful} successful, {failed} failed)")


def _commit_batch(coll, batch: List[dict]) -> None:
    """Commit a batch of updates to MongoDB."""
    from bson import ObjectId

    for item in batch:
        coll.update_one(
            {"_id": ObjectId(item["id"])},
            {"$set": {
                "categories": item["categories"],
                "tags": item["tags"]
            }},
        )
        cat_str = ", ".join(
            item["categories"]) if item["categories"] else "none"
        tag_str = ", ".join(item["tags"][:3]) + \
            ("..." if len(item["tags"]) > 3 else "")
        print(f"[OK] {item['title'][:50]} → [{cat_str}] | {tag_str}")
