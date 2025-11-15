#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

SOLR_URL = "http://localhost:8983/solr/ikea_hacks"

def load_json_file(filepath):
    """Load items from a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return []

def prepare_document(item, source):
    """Prepare a document for Solr indexing"""
    
    # Generate unique ID (use URL or create one)
    doc_id = item.get('url', f"{source}_{hash(str(item))}")
    
    doc = {
        "id": doc_id,
        "title": item.get('title', 'Untitled'),
        "content": item.get('content', ''),
        "author": item.get('author', 'Unknown'),
        "url": item.get('url', ''),
        "excerpt": item.get('excerpt', ''),
    }
    
    # Handle date field (can be None)
    if item.get('date'):
        doc['date'] = item['date']
    
    # Handle image URL
    if item.get('image_url'):
        doc['image_url'] = item['image_url']
    
    # Handle multi-valued fields (ensure they're lists)
    categories = item.get('categories', [])
    if isinstance(categories, str):
        categories = [categories]
    doc['categories'] = categories if categories else []
    
    tags = item.get('tags', [])
    if isinstance(tags, str):
        tags = [tags]
    doc['tags'] = tags if tags else []
    
    return doc

def index_documents(documents):
    """Index documents to Solr"""
    if not documents:
        return False
    
    url = f"{SOLR_URL}/update?commit=true"
    
    try:
        response = requests.post(
            url,
            json=documents,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"   ✅ Indexed {len(documents)} documents")
            return True
        else:
            print(f"   ❌ Indexing failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error indexing: {e}")
        return False

def clear_collection():
    """Clear all documents from the collection (optional)"""
    url = f"{SOLR_URL}/update?commit=true"
    delete_all = {"delete": {"query": "*:*"}}
    
    try:
        response = requests.post(url, json=delete_all)
        if response.status_code == 200:
            print("🗑️  Cleared existing documents")
            return True
    except Exception as e:
        print(f"⚠️  Could not clear collection: {e}")
        return False

def index_all_data():
    """Index all JSON files from the data directory"""
    
    print("=" * 60)
    print("Indexing IKEA Hacks data to Solr")
    print("=" * 60)
    print()
    
    # Check Solr connection
    try:
        response = requests.get(f"{SOLR_URL}/admin/ping")
        if response.status_code != 200:
            print("❌ Cannot reach Solr")
            return False
        print("✅ Connected to Solr")
    except Exception as e:
        print(f"❌ Cannot connect to Solr: {e}")
        return False
    
    print()
    
    # Optional: clear existing data
    # clear_collection()
    # print()
    
    data_dir = "ikea_hacks_scraper/data"
    
    json_files = [
        ("ikea_hacks.json", "ikea"),
        ("tosize_hacks.json", "tosize"),
        ("loveproperty_hacks.json", "loveproperty")
    ]
    
    all_documents = []
    total_loaded = 0
    
    for json_file, source in json_files:
        filepath = os.path.join(data_dir, json_file)
        
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
        
        print(f"📂 Loading: {json_file}")
        items = load_json_file(filepath)
        
        if not items:
            print(f"   ⚠️  No items found in {json_file}")
            continue
        
        for item in items:
            doc = prepare_document(item, source)
            all_documents.append(doc)
        
        print(f"   Loaded {len(items)} items")
        total_loaded += len(items)
    
    print()
    print(f"📊 Total documents to index: {len(all_documents)}")
    print()
    
    if not all_documents:
        print("❌ No documents to index!")
        return False
    
    # Index in batches of 100
    batch_size = 100
    batches = (len(all_documents) + batch_size - 1) // batch_size
    
    print(f"Indexing in {batches} batch(es)...")
    print()
    
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i+batch_size]
        batch_num = i//batch_size + 1
        print(f"Batch {batch_num}/{batches}:")
        index_documents(batch)
    
    print()
    print("=" * 60)
    print("✅ Indexing complete!")
    print("=" * 60)
    print()
    print(f"📊 Total documents indexed: {len(all_documents)}")
    print(f"🔍 View all: {SOLR_URL}/select?q=*:*&rows=10")
    print(f"🌐 Admin UI: http://localhost:8983/solr/#/ikea_hacks/query")
    print()

if __name__ == "__main__":
    index_all_data()