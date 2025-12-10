
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv("vinyl_scout/.env")
TOKEN = os.getenv("DISCOGS_TOKEN")

headers = {
    "Authorization": f"Discogs token={TOKEN}",
    "User-Agent": "VinylScout/1.0"
}

def check_prices(query):
    print(f"Searching for: {query}")
    # 1. Search
    search_url = f"https://api.discogs.com/database/search?q={query}&type=release" 
    resp = requests.get(search_url, headers=headers)
    data = resp.json()
    
    if not data['results']:
        print("No results found.")
        return

    first_hit = data['results'][0]
    release_id = first_hit['id']
    print(f"Found Release: {first_hit['title']} (ID: {release_id})")
    
    # 2. Check Price Suggestions
    print("\nChecking Price Suggestions...")
    sugg_url = f"https://api.discogs.com/marketplace/price_suggestions/{release_id}"
    resp = requests.get(sugg_url, headers=headers)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=2))
    else:
        print(f"Error {resp.status_code}: {resp.text}")

    # 3. Check Marketplace Stats (likely 404 or auth protected differently)
    print("\nChecking Marketplace Stats...")
    stats_url = f"https://api.discogs.com/marketplace/stats/{release_id}"
    resp = requests.get(stats_url, headers=headers)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=2))
    else:
        print(f"Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    check_prices("Marvin Gaye What's Going On")
