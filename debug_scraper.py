
import os
import logging
import json
from scraper import get_vinyl_data, scrape_ebay_sold, search_discogs, scrape_popsike

# Setup logging to see what's happening
logging.basicConfig(level=logging.DEBUG)

def debug_search(query):
    print(f"\n--- Debugging Search: '{query}' ---")
    
    print("\n1. Testing Discogs API...")
    try:
        discogs_data = search_discogs(query)
        print("Discogs Result:")
        print(json.dumps(discogs_data, indent=2))
    except Exception as e:
        print(f"Discogs FAILED: {e}")

    print("\n2. Testing eBay Scraper...")
    try:
        ebay_data = scrape_ebay_sold(query)
        print("eBay Result:")
        print(json.dumps(ebay_data, indent=2) if ebay_data else "None (Scraper returned empty)")
    except Exception as e:
        print(f"eBay FAILED: {e}")

    print("\n3. Testing Popsike Scraper...")
    try:
        popsike_data = scrape_popsike(query)
        print("Popsike Result:")
        print(json.dumps(popsike_data, indent=2) if popsike_data else "None (Scraper returned empty)")
    except Exception as e:
        print(f"Popsike FAILED: {e}")

if __name__ == "__main__":
    # Test the specific query user mentioned
    debug_search("Daft Punk Random Access Memories")
