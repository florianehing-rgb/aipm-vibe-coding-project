
import os
import time
import json
import logging
import requests
from bs4 import BeautifulSoup
from functools import wraps
from datetime import datetime, timedelta
from dotenv import load_dotenv
import urllib.parse
import re

load_dotenv()

DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
CACHE_FILE = "search_cache.json"
CACHE_DURATION_MINUTES = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cached_data(key):
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
            
            if key in cache:
                timestamp = datetime.fromisoformat(cache[key]['timestamp'])
                if datetime.now() - timestamp < timedelta(minutes=CACHE_DURATION_MINUTES):
                    logger.info(f"Cache hit for {key}")
                    return cache[key]['data']
    except Exception as e:
        logger.error(f"Cache read error: {e}")
    return None

def save_to_cache(key, data):
    try:
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                try:
                    cache = json.load(f)
                except json.JSONDecodeError:
                    pass
        
        cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
            
    except Exception as e:
        logger.error(f"Cache write error: {e}")

def search_discogs(query):
    if not DISCOGS_TOKEN:
        logger.warning("No Discogs token found")
        return None

    headers = {
        "Authorization": f"Discogs token={DISCOGS_TOKEN}",
        "User-Agent": "VinylScout/1.0"
    }
    
    try:
        # Search for release
        search_url = f"https://api.discogs.com/database/search?q={urllib.parse.quote(query)}&type=release"
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if not data['results']:
            # Try master if release not found
            search_url = f"https://api.discogs.com/database/search?q={urllib.parse.quote(query)}&type=master"
            response = requests.get(search_url, headers=headers)
            data = response.json()
            
        if data['results']:
            best_match = data['results'][0]
            release_id = best_match['id']
            
            # Basic Info
            stats = {
                'title': best_match.get('title'),
                'year': best_match.get('year'),
                'cover_image': best_match.get('cover_image'),
                'url': f"https://www.discogs.com{best_match.get('uri')}",
                'format': best_match.get('format', []),
                'prices': {},
                'marketplace': {}
            }
            
            # Get Price Suggestions
            try:
                sugg_url = f"https://api.discogs.com/marketplace/price_suggestions/{release_id}"
                sugg_resp = requests.get(sugg_url, headers=headers)
                if sugg_resp.status_code == 200:
                    stats['prices'] = sugg_resp.json()
            except Exception as e:
                logger.error(f"Discogs Price Suggestion Error: {e}")

            # Get Marketplace Stats
            try:
                stats_url = f"https://api.discogs.com/marketplace/stats/{release_id}"
                stats_resp = requests.get(stats_url, headers=headers)
                if stats_resp.status_code == 200:
                    stats['marketplace'] = stats_resp.json()
            except Exception as e:
                logger.error(f"Discogs Stats Error: {e}")
                
            return stats
            
    except Exception as e:
        logger.error(f"Discogs API error: {e}")
        return None

def scrape_ebay_sold(query):
    # Try with robust headers
    query += " vinyl record"
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_query}&LH_Sold=1&LH_Complete=1&_ipg=60"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = []
        # Try multiple selector variations for eBay
        listings = soup.select('.s-item__wrapper')
        if not listings:
             listings = soup.select('li.s-item')
        
        prices = []
        
        for item in listings:
            if "s-item__no-title" in str(item): continue
                
            title_elem = item.select_one('.s-item__title')
            price_elem = item.select_one('.s-item__price')
            link_elem = item.select_one('.s-item__link')
            date_elem = item.select_one('.s-item__title--tagspan .POSITIVE') # Sold date status
            
            if title_elem and price_elem:
                title = title_elem.get_text(strip=True)
                price_str = price_elem.get_text(strip=True)
                link = link_elem['href'] if link_elem else "#"
                
                try:
                    # Clean price - handle usually "$20.00" or similar
                    # Remove "Sold" text etc
                    clean_price = float(''.join(c for c in price_str if c.isdigit() or c == '.'))
                    prices.append(clean_price)
                    
                    items.append({
                        'title': title,
                        'price': price_str,
                        'price_val': clean_price,
                        'link': link
                    })
                except ValueError:
                    continue
        
        if not prices:
            return None

        avg_price = sum(prices) / len(prices)
        
        return {
            'sold_listings': items[:5],
            'stats': {
                'average_price': round(avg_price, 2),
                'min_price': min(prices),
                'max_price': max(prices),
                'count': len(prices)
            }
        }

    except Exception as e:
        logger.error(f"eBay scraping error: {e}")
        return None

def scrape_popsike(query):
    encoded_query = urllib.parse.quote(query.replace(" ", "+"))
    # sortord=dprice means Sort by Price (Desc) usually, but we might want recent? 
    # Let's use dprice (Desc Price) or ddate (Desc Date)? Defaulting to dprice as requested 
    # but maybe ddate is better for market trends?
    # Popsike default seems to be relevant. Let's try to get high value items.
    url = f"https://www.popsike.com/php/quicksearch.php?searchtext={encoded_query}&sortord=dprice"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = []
        # Based on debug html, items are in <div class="item-list make-list"><div class="row">...
        # Each Item is effectively a row inside item-list make-list, but let's be careful.
        # It seems .add-desc-box contains the title.
        
        rows = soup.select('.item-list.make-list .row')
        
        for row in rows:
            try:
                # Title
                title_elem = row.select_one('.add-title a')
                if not title_elem: continue
                title = title_elem.get_text(strip=True)
                link = title_elem['href']
                if not link.startswith('http'):
                    link = f"https://www.popsike.com/{link}" if link.startswith('..') else link

                # Date
                date_elem = row.select_one('.date')
                date_str = date_elem.get_text(strip=True) if date_elem else "Unknown Date"
                # Cleanup date - remove the "Favourite Auctions..." pollution
                # Look for standard date format like "Jul 14, 2023" or "2023-07-14"
                # The pollution ends with "register", so we could split by that, or just regex search for date
                date_match = re.search(r'([A-Z][a-z]{2}\s\d{1,2},\s\d{4})', date_str)
                if date_match:
                    date_str = date_match.group(1)
                else:
                     # Fallback cleanup if regex fails but we know it's messy
                     if "register" in date_str:
                         date_str = date_str.split("register")[-1].strip()
 

                # Price
                price_box = row.select_one('.price-box .item-price')
                if not price_box: continue
                
                # Price is messy in the HTML table structure
                # We can just extract all text and find the numbers
                price_text = price_box.get_text(strip=True)
                # Usually contains £ 1,200 or $ 1,590
                # Let's try to grab the USD value if present, or just the first number
                
                # Regex for price
                # e.g. 1,590
                price_matches = re.findall(r'[\d,]+', price_text)
                if not price_matches: continue
                
                price_val_str = price_matches[-1] # Usually the last one is the USD or main currency?
                price_val = float(price_val_str.replace(',', ''))
                
                items.append({
                    'title': title,
                    'date': date_str,
                    'price': f"${price_val:,.2f}",
                    'link': link,
                    'price_val': price_val
                })
                
            except Exception as e:
                continue
                
        if not items:
            return None
            
        return {
            'listings': items[:5], # Top 5 results
            'count': len(items)
        }

    except Exception as e:
        logger.error(f"Popsike scraping error: {e}")
        return None

def get_vinyl_data(query):
    # Check cache first
    cached = get_cached_data(query)
    if cached:
        return cached

    # Fetch fresh data
    discogs_data = search_discogs(query)
    ebay_data = scrape_ebay_sold(query)
    popsike_data = scrape_popsike(query)
    
    result = {
        'query': query,
        'discogs': discogs_data,
        'ebay': ebay_data,
        'popsike': popsike_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Cache if we got anything useful
    if discogs_data or ebay_data or popsike_data:
        save_to_cache(query, result)
        
    return result
