#!/usr/bin/env python3
import requests
import json

SOLR_URL = "http://localhost:8983/solr/ikea_hacks"

def add_field(field_name, field_type, stored=True, indexed=True, multiValued=False):
    """Add a field to the Solr schema"""
    url = f"{SOLR_URL}/schema"
    
    field_def = {
        "name": field_name,
        "type": field_type,
        "stored": stored,
        "indexed": indexed,
        "multiValued": multiValued
    }
    
    data = {"add-field": field_def}
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f"✅ Added field: {field_name} ({field_type})")
            return True
        elif "already exists" in response.text:
            print(f"⚠️  Field already exists: {field_name}")
            return True
        else:
            print(f"❌ Failed to add {field_name}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding {field_name}: {e}")
        return False

def setup_schema():
    """Set up the complete schema for IKEA hacks"""
    
    print("=" * 60)
    print("Setting up Solr schema for IKEA hacks collection")
    print("=" * 60)
    print()
    
    # Check if Solr is reachable
    try:
        response = requests.get(f"{SOLR_URL}/admin/ping")
        if response.status_code != 200:
            print("❌ Cannot reach Solr. Make sure it's running on http://localhost:8983")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Solr: {e}")
        print("Make sure Solr is running: bin/solr start")
        return False
    
    print("✅ Connected to Solr")
    print()
    
    # Define all fields
    # Format: (field_name, field_type, stored, indexed, multiValued)
    fields = [
        # Text fields (full-text searchable)
        ("title", "text_general", True, True, False),
        ("content", "text_general", True, True, False),
        ("excerpt", "text_general", True, True, False),
        
        # String fields (exact match, for filtering/faceting)
        ("author", "string", True, True, False),
        ("url", "string", True, False, False),  # Not indexed (just stored for display)
        ("image_url", "string", True, False, False),
        
        # Date field
        ("date", "pdate", True, True, False),
        
        # Multi-valued string fields (arrays)
        ("categories", "string", True, True, True),
        ("tags", "string", True, True, True),
    ]
    
    print("Adding fields to schema...")
    print()
    
    success_count = 0
    for field_name, field_type, stored, indexed, multi in fields:
        if add_field(field_name, field_type, stored, indexed, multi):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"Schema setup complete! ({success_count}/{len(fields)} fields)")
    print("=" * 60)
    print()
    print(f"📊 View schema: {SOLR_URL}/schema")
    print(f"🔍 Admin UI: http://localhost:8983/solr/#/ikea_hacks")
    print()
    
    return True

if __name__ == "__main__":
    setup_schema()