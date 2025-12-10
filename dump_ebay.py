
import requests
import urllib.parse
from bs4 import BeautifulSoup

# Try active listings first to see if we can get ANY items
query = "Marvin Gaye What's Going On vinyl record"
encoded_query = urllib.parse.quote(query)
# Active listings URL
url = f"https://www.ebay.com/sch/i.html?_nkw={encoded_query}&_ipg=60"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
items = soup.select('.s-item__wrapper')
print(f"Found {len(items)} items")

with open("ebay_debug_v2.html", "w") as f:
    f.write(response.text)
