#!/usr/bin/env python3
import requests
import json

SOLR_URL = "http://localhost:8983/solr/ikea_hacks"

def search(query, rows=5, fields="id,title,author,score"):
    """Perform a search query"""
    url = f"{SOLR_URL}/select"
    
    # Search across multiple fields explicitly
    # Use dismax query parser for better text search
    params = {
        "q": query,
        "rows": rows,
        "fl": fields,
        "defType": "edismax",  # Extended DisMax query parser
        "qf": "title^3 content^2 excerpt author categories tags",  # Query fields with boosting
        "df": "_text_"  # Default field
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        num_found = data['response']['numFound']
        docs = data['response']['docs']
        
        print(f"\n{'='*60}")
        print(f"Search query: '{query}'")
        print(f"Found: {num_found} results")
        print('='*60)
        
        if docs:
            for i, doc in enumerate(docs, 1):
                print(f"\n{i}. {doc.get('title', 'No title')}")
                print(f"   Author: {doc.get('author', 'Unknown')}")
                print(f"   Score: {doc.get('score', 0):.4f}")
                print(f"   ID: {doc.get('id', 'N/A')[:60]}...")
        else:
            print("\nNo results found.")
        
        print()
        return num_found
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return 0
    

def test_searches():
    """Run a series of test searches"""
    print("\n" + "="*60)
    print("Testing Solr Search Functionality")
    print("="*60)
    
    # Test 1: Simple keyword search
    search("kallax")
    
    # Test 2: Multi-word search
    search("bedroom storage")
    
    # Test 3: Product name
    search("billy bookcase")
    
    # Test 4: Technique
    search("paint")
    
    # Test 5: Everything (wildcard)
    total = search("*:*", rows=3)
    
    print("="*60)
    print(f"✅ All tests complete! Total docs in index: {total}")
    print("="*60)
    print()

if __name__ == "__main__":
    test_searches()