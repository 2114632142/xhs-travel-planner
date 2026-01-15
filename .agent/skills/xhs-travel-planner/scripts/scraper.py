#!/usr/bin/env python3
"""
XHS (Xiaohongshu) Scraper with Patchright
==========================================
Scrapes travel-related notes from Xiaohongshu with anti-detection measures.

Usage:
    python scraper.py --login                    # First-time login (saves cookies)
    python scraper.py --query "黄山" --limit 30  # Search and scrape
"""

import asyncio
import json
import random
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

try:
    from patchright.async_api import async_playwright
except ImportError:
    print("Error: pip install patchright")
    sys.exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
COOKIES_FILE = Path.home() / ".xhs_cookies.json"
OUTPUT_DIR = SKILL_DIR / "output"
KEYWORDS_FILE = SKILL_DIR / "references" / "keywords.json"

# Config
XHS_URL = "https://www.xiaohongshu.com"
XHS_SEARCH_URL = "https://www.xiaohongshu.com/search_result"


class XHSScraper:
    def __init__(self):
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None
        self.results = []

    async def start(self, headless=False):
        """Launch browser with stealth settings."""
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            headless=headless,
            channel='chrome',
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-first-run'
            ]
        )
        
        # Create context with realistic viewport
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Load cookies if exists
        if COOKIES_FILE.exists():
            cookies = json.loads(COOKIES_FILE.read_text(encoding='utf-8'))
            await self.context.add_cookies(cookies)
            print(f"[INFO] Loaded cookies from {COOKIES_FILE}")
        
        self.page = await self.context.new_page()
        return self

    async def close(self):
        """Close browser and save cookies."""
        if self.context:
            cookies = await self.context.cookies()
            COOKIES_FILE.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"[INFO] Cookies saved to {COOKIES_FILE}")
        if self.browser:
            await self.browser.close()
        if self.pw:
            await self.pw.stop()

    async def login(self):
        """Open XHS for manual login."""
        print("[INFO] Opening XHS for login...")
        print("[INFO] Please log in manually. Press Enter when done.")
        
        await self.page.goto(XHS_URL, wait_until='networkidle', timeout=60000)
        
        # Wait for user to login
        input("\n>>> Press Enter after you have logged in...\n")
        
        # Verify login by checking for user avatar or profile element
        await asyncio.sleep(2)
        print("[INFO] Login saved. You can now run searches.")

    async def _random_delay(self, min_sec=3, max_sec=8):
        """Human-like random delay."""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)

    async def _scroll_page(self):
        """Simulate human scrolling."""
        for _ in range(random.randint(2, 4)):
            await self.page.evaluate(f"window.scrollBy(0, {random.randint(300, 600)})")
            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def search(self, query: str, limit: int = 30):
        """Search XHS and extract note cards."""
        print(f"[INFO] Searching for: {query}")
        
        # Navigate to search
        search_url = f"{XHS_SEARCH_URL}?keyword={query}&source=web_search_result_notes"
        await self.page.goto(search_url, wait_until='networkidle', timeout=30000)
        await self._random_delay(2, 4)
        
        # Check for login wall
        if "login" in self.page.url.lower():
            print("[ERROR] Login required. Run with --login first.")
            return []
        
        notes = []
        page_count = 0
        
        while len(notes) < limit:
            page_count += 1
            print(f"[INFO] Scraping page {page_count}, collected {len(notes)} notes...")
            
            # Extract note cards from current view
            cards = await self.page.query_selector_all('section.note-item, div[data-v-a264b01a].note-item, .feeds-page .note-item')
            
            if not cards:
                # Try alternative selectors
                cards = await self.page.query_selector_all('[class*="note"]')
            
            for card in cards:
                if len(notes) >= limit:
                    break
                
                try:
                    # Extract title
                    title_el = await card.query_selector('.title, span.title, [class*="title"]')
                    title = await title_el.inner_text() if title_el else ""
                    
                    # Extract author
                    author_el = await card.query_selector('.author, .name, [class*="author"], [class*="name"]')
                    author = await author_el.inner_text() if author_el else ""
                    
                    # Extract link
                    link_el = await card.query_selector('a')
                    link = await link_el.get_attribute('href') if link_el else ""
                    if link and not link.startswith('http'):
                        link = f"https://www.xiaohongshu.com{link}"
                    
                    # Extract likes/engagement
                    likes_el = await card.query_selector('[class*="like"], [class*="count"]')
                    likes = await likes_el.inner_text() if likes_el else "0"
                    
                    if title and title not in [n['title'] for n in notes]:
                        notes.append({
                            'title': title.strip(),
                            'author': author.strip(),
                            'link': link,
                            'likes': likes.strip(),
                            'query': query
                        })
                        
                except Exception as e:
                    continue
            
            # Scroll to load more
            await self._scroll_page()
            await self._random_delay(3, 6)
            
            # Check for end of results
            old_count = len(notes)
            await asyncio.sleep(2)
            if len(notes) == old_count and page_count > 3:
                print("[INFO] No more new notes found.")
                break
            
            # Rest every 10 notes
            if len(notes) % 10 == 0 and len(notes) > 0:
                print(f"[INFO] Resting for 30 seconds to avoid detection...")
                await asyncio.sleep(30)
        
        self.results.extend(notes)
        return notes

    async def search_multiple(self, destination: str, limit_per_query: int = 10):
        """Search with multiple keyword templates."""
        if KEYWORDS_FILE.exists():
            config = json.loads(KEYWORDS_FILE.read_text(encoding='utf-8'))
            templates = config.get('search_templates', [])
        else:
            templates = ["{destination} 攻略"]
        
        all_notes = []
        for template in templates:
            query = template.format(destination=destination)
            notes = await self.search(query, limit=limit_per_query)
            all_notes.extend(notes)
            await self._random_delay(5, 10)  # Longer delay between queries
        
        return all_notes

    def save_results(self, filename: str = None):
        """Save results to JSON file."""
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xhs_results_{timestamp}.json"
        
        output_path = OUTPUT_DIR / filename
        output_path.write_text(
            json.dumps(self.results, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        print(f"[INFO] Results saved to {output_path}")
        return output_path


async def main():
    parser = argparse.ArgumentParser(description="XHS Travel Scraper")
    parser.add_argument("--login", action="store_true", help="Login mode (saves cookies)")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--destination", type=str, help="Destination for multi-query search")
    parser.add_argument("--limit", type=int, default=30, help="Max notes to scrape")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    scraper = XHSScraper()
    
    try:
        # Login mode should never be headless
        await scraper.start(headless=False if args.login else args.headless)
        
        if args.login:
            await scraper.login()
        elif args.destination:
            await scraper.search_multiple(args.destination, limit_per_query=args.limit // 6)
            scraper.save_results()
        elif args.query:
            await scraper.search(args.query, limit=args.limit)
            scraper.save_results()
        else:
            print("Usage: python scraper.py --login | --query <query> | --destination <destination>")
    
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
