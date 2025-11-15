#!/usr/bin/env python3
import requests
import json

SOLR_URL = "http://localhost:8983/solr/ikea_hacks"

def check_solr_status():
    """Check if Solr is running and accessible"""
    print("\n" + "="*60)
    print("1. CHECKING SOLR STATUS")
    print("="*60)
    
    try:
        response = requests.get(f"{SOLR_URL}/admin/ping", timeout=5)
        if response.status_code == 200:
            print("✅ Solr is running and accessible")
            return True
        else:
            print(f"❌ Solr returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Solr: {e}")
        return False

def check_document_count():
    """Check total number of documents in Solr"""
    print("\n" + "="*60)
    print("2. CHECKING DOCUMENT COUNT")
    print("="*60)
    
    url = f"{SOLR_URL}/select"
    params = {"q": "*:*", "rows": 0}  # rows=0 means just get count
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        num_docs = data['response']['numFound']
        
        print(f"📊 Total documents in Solr: {num_docs}")
        
        if num_docs == 265:
            print("✅ Correct! Expected 265 (203+20+42)")
        elif num_docs == 0:
            print("❌ No documents! Need to run: python3 index_data_to_solr.py")
        else:
            print(f"⚠️  Expected 265, found {num_docs}")
        
        return num_docs
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

def check_document_by_source():
    """Count documents from each source"""
    print("\n" + "="*60)
    print("3. CHECKING DOCUMENTS BY SOURCE")
    print("="*60)
    
    sources = [
        ("ikeahackers.net", "IKEA Hackers"),
        ("tosize.it", "Tosize"),
        ("loveproperty.com", "Love Property")
    ]
    
    for domain, name in sources:
        url = f"{SOLR_URL}/select"
        params = {
            "q": f"url:*{domain}*",
            "rows": 0
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            count = data['response']['numFound']
            print(f"📁 {name}: {count} documents")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

def sample_random_documents(num_samples=3):
    """Fetch and display random documents"""
    print("\n" + "="*60)
    print("4. SAMPLING RANDOM DOCUMENTS FROM SOLR")
    print("="*60)
    
    url = f"{SOLR_URL}/select"
    params = {
        "q": "*:*",
        "rows": num_samples,
        "sort": "random_" + str(hash("seed")) + " asc",  # Pseudo-random
        "fl": "id,title,author,url,categories,tags"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        docs = data['response']['docs']
        
        print(f"Showing {len(docs)} random documents:\n")
        
        for i, doc in enumerate(docs, 1):
            print(f"--- Document {i} ---")
            print(f"Title: {doc.get('title', 'N/A')[:70]}")
            print(f"Author: {doc.get('author', 'N/A')}")
            print(f"URL: {doc.get('url', 'N/A')[:70]}")
            print(f"Categories: {doc.get('categories', [])}")
            print(f"Tags: {doc.get('tags', [])[:5]}")  # First 5 tags
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def check_specific_field_coverage():
    """Check which fields have data"""
    print("\n" + "="*60)
    print("5. CHECKING FIELD COVERAGE")
    print("="*60)
    
    fields = ["title", "content", "author", "date", "categories", "tags"]
    
    for field in fields:
        url = f"{SOLR_URL}/select"
        params = {
            "q": f"{field}:*",  # Documents where field exists and is not empty
            "rows": 0
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            count = data['response']['numFound']
            percentage = (count / 265) * 100 if count > 0 else 0
            
            status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
            print(f"{status} {field}: {count}/265 ({percentage:.1f}%)")
        except Exception as e:
            print(f"❌ {field}: Error - {e}")

def main():
    print("\n" + "="*70)
    print("SOLR SYSTEM VERIFICATION")
    print("="*70)
    
    # Run all checks
    if not check_solr_status():
        print("\n❌ Solr is not running! Start it with: ~/solr-9.7.0/bin/solr start")
        return
    
    doc_count = check_document_count()
    
    if doc_count == 0:
        print("\n❌ No documents indexed! Run: python3 index_data_to_solr.py")
        return
    
    check_document_by_source()
    sample_random_documents(3)
    check_specific_field_coverage()
    
    print("\n" + "="*70)
    print("✅ VERIFICATION COMPLETE")
    print("="*70)
    print()

if __name__ == "__main__":
    main()