# Vinyl Scout - Agent Instructions

## Project Overview
Vinyl Scout is a Flask-based web application for real-time vinyl record valuation. It aggregates pricing data from Discogs (API), eBay (Scraping), and Popsike (Scraping) to provide a comprehensive market view.

## Architecture

### Backend (`app.py`)
- **Framework**: Flask
- **Database**: SQLite (via SQLAlchemy) for search history.
- **Search Strategy**:
  - Initial load requests basic page structure.
  - Search form submits via AJAX (`?partial=true`).
  - Server renders `templates/partials/results_content.html` and returns it as a fragment.

### Scrapers (`scraper.py`)
- **Discogs**: Uses official API. Requires `DISCOGS_TOKEN` in `.env`.
- **eBay**: Scrapes "Sold Listings".
  - **Critical**: Must use robust headers (User-Agent, Sec-Fetch-*) to avoid bot detection.
  - **Selectors**: Looks for `.s-item__wrapper` or `li.s-item`.
- **Popsike**: Scrapes public search results.
  - **Strategy**: Parses HTML table rows (`.item-list.make-list .row`).
  - **Date Parsing**: Date strings often contain "Favourite Auctions" modal text pollution; must be cleaned via regex.

### Frontend
- **Styling**: TailwindCSS (via CDN).
- **Templates**: Jinja2.
  - `base.html`: Layout skeleton.
  - `index.html`: Main page + AJAX logic.
  - `results.html`: Legacy full-page render (wrapper).
  - `partials/results_content.html`: Core results grid (used for dynamic updates).

## Key Files
- `app.py`: Main entry point.
- `scraper.py`: All data fetching logic.
- `debug_scraper.py`: Standalone script to verify scrapers without running the full Flask app.
- `requirements.txt`: Python dependencies (`flask`, `requests`, `beautifulsoup4`, `python-dotenv`).

## Common Tasks / Patterns

### Adding a New Source
1.  Add scraper function in `scraper.py` (e.g., `scrape_source(query)`).
2.  Update `get_vinyl_data` to call the new scraper.
3.  Update `requirements.txt` if new libs are needed.
4.  Update `templates/partials/results_content.html` to display the data.

### Verification
- **Quick Test**: Run `python debug_scraper.py` to check if scrapers are being blocked.
- **Full Test**: Run `python app.py` (port 5000) and perform a search in the browser.

## Known Issues
- **Rate Limiting**: eBay and Popsike may block IPs if scraped too aggressively.
- **DOM Changes**: Scrapers are fragile. If stats return 0 or "None", check `debug_scraper.py` and inspect the target site's HTML.
