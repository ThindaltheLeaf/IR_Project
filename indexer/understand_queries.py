#!/usr/bin/env python3
import requests
import json

SOLR_URL = "http://localhost:8983/solr/ikea_hacks"

def explain_query(query_term):
    """Show how a query works step by step"""
    print("\n" + "="*70)
    print(f"QUERY: '{query_term}'")
    print("="*70)
    
    url = f"{SOLR_URL}/select"
    
    # The actual query parameters
    params = {
        "q": query_term,
        "defType": "edismax",
        "qf": "title^3 content^2 excerpt^1.5 author categories tags",
        "rows": 5,
        "fl": "id,title,author,score",
        "debugQuery": "true"  # Get debug info
    }
    
    print("\n📋 Query Parameters:")
    print(f"  • Query term: {query_term}")
    print(f"  • Parser: edismax (Extended DisMax)")
    print(f"  • Search fields:")
    print(f"    - title (weight: 3x)")
    print(f"    - content (weight: 2x)")
    print(f"    - excerpt (weight: 1.5x)")
    print(f"    - author, categories, tags (weight: 1x)")
    print(f"  • Results to return: 5")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        num_found = data['response']['numFound']
        docs = data['response']['docs']
        
        print(f"\n📊 Results: Found {num_found} matching documents")
        
        if docs:
            print(f"\n🔝 Top 5 Results:\n")
            for i, doc in enumerate(docs, 1):
                print(f"{i}. {doc.get('title', 'No title')[:65]}")
                print(f"   👤 Author: {doc.get('author', 'Unknown')}")
                print(f"   ⭐ Relevance Score: {doc.get('score', 0):.4f}")
                print()
            
            # Show why the top result matched
            if 'debug' in data and 'explain' in data['debug']:
                print("💡 Why did the top result rank highest?")
                top_doc_id = docs[0]['id']
                explain_text = data['debug']['explain'].get(top_doc_id, '')
                
                # Simplify explanation
                if 'title' in explain_text:
                    print("   ✓ Term found in TITLE (3x boost)")
                if 'content' in explain_text:
                    print("   ✓ Term found in CONTENT (2x boost)")
                if 'excerpt' in explain_text:
                    print("   ✓ Term found in EXCERPT (1.5x boost)")
                print()
        else:
            print("\n❌ No results found for this query")
        
        # Show the actual Solr URL
        query_params = "&".join([f"{k}={v}" for k, v in params.items() if k != "debugQuery"])
        print(f"🔗 Full Solr URL:")
        print(f"   {url}?{query_params}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def compare_queries():
    """Compare different query types"""
    print("\n" + "="*70)
    print("COMPARING DIFFERENT QUERY TYPES")
    print("="*70)
    
    queries = [
        ("kallax", "Single word - common product name"),
        ("bedroom storage", "Two words - finds documents with both"),
        ("paint AND wood", "Boolean AND - must have both terms"),
        ("title:kallax", "Field-specific - only search in title"),
        ("author:Jules", "Search by author"),
        ("categories:bedroom", "Search by category"),
    ]
    
    for query, description in queries:
        url = f"{SOLR_URL}/select"
        params = {
            "q": query,
            "defType": "edismax",
            "qf": "title^3 content^2 excerpt^1.5 author categories tags",
            "rows": 0  # Just get count
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            count = data['response']['numFound']
            
            print(f"\n'{query}'")
            print(f"  {description}")
            print(f"  📊 Results: {count} documents")
        except Exception as e:
            print(f"  ❌ Error: {e}")

def show_query_flow():
    """Visualize the query flow"""
    print("\n" + "="*70)
    print("HOW A QUERY FLOWS THROUGH THE SYSTEM")
    print("="*70)
    
    print("""
1. USER INTERFACE (your teammate builds this)
   └─> User types: "bedroom storage"
   
2. INTERFACE SENDS HTTP REQUEST
   └─> GET http://localhost:8983/solr/ikea_hacks/select?
       q=bedroom storage
       &defType=edismax
       &qf=title^3 content^2 excerpt^1.5 author categories tags
       &rows=20
   
3. SOLR RECEIVES REQUEST
   └─> Parses query with Extended DisMax parser
   └─> Searches across specified fields (title, content, etc.)
   └─> Applies field boosting (title=3x, content=2x)
   └─> Calculates relevance scores
   
4. SOLR RETURNS JSON RESPONSE
   └─> {
         "response": {
           "numFound": 106,
           "docs": [
             {
               "id": "...",
               "title": "This Clever PAX Wardrobe Hack...",
               "author": "Stacy Randall",
               "score": 6.2013,
               "url": "https://...",
               ...
             },
             ...
           ]
         }
       }
   
5. INTERFACE DISPLAYS RESULTS
   └─> Shows titles, authors, snippets
   └─> Adds pagination, filters, etc.
   └─> User clicks on result → opens URL
    """)

def main():
    print("\n" + "="*70)
    print("UNDERSTANDING SOLR QUERIES")
    print("="*70)
    
    # Explain individual queries
    explain_query("kallax")
    explain_query("bedroom storage")
    explain_query("paint")
    
    # Compare query types
    compare_queries()
    
    # Show flow
    show_query_flow()
    
    print("\n" + "="*70)
    print("✅ QUERY EXPLANATION COMPLETE")
    print("="*70)
    print()

if __name__ == "__main__":
    main()