#!/usr/bin/env python3
import json

def inspect_json_file(filepath, num_samples=2):
    """Inspect contents of a JSON file"""
    print(f"\n{'='*60}")
    print(f"Inspecting: {filepath}")
    print('='*60)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total items: {len(data)}")
    print(f"\nShowing first {num_samples} items:\n")
    
    for i, item in enumerate(data[:num_samples], 1):
        print(f"--- Item {i} ---")
        print(f"Title: {item.get('title', 'N/A')[:80]}")
        print(f"Author: {item.get('author', 'N/A')}")
        print(f"URL: {item.get('url', 'N/A')[:80]}")
        print(f"Content length: {len(item.get('content', ''))} characters")
        print(f"Categories: {item.get('categories', [])}")
        print(f"Tags: {item.get('tags', [])}")
        print(f"Date: {item.get('date', 'N/A')}")
        print()

if __name__ == "__main__":
    inspect_json_file("ikea_hacks_scraper/data/ikea_hacks.json", 2)
    inspect_json_file("ikea_hacks_scraper/data/tosize_hacks.json", 1)
    inspect_json_file("ikea_hacks_scraper/data/loveproperty_hacks.json", 1)