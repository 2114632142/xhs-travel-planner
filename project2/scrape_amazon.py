import time
import json
import random
from patchright.sync_api import sync_playwright

def scrape_amazon_jbl():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        products = []
        search_url = "https://www.amazon.co.jp/s?k=JBL"
        
        for i in range(1, 6):
            print(f"Scraping page {i}...")
            url = f"{search_url}&page={i}"
            try:
                page.goto(url, wait_until="load")
                time.sleep(random.uniform(3, 6))
                
                # Check for bot detection
                if "captcha" in page.url().lower() or "dog" in page.title().lower() or "验证码" in page.content():
                    print(f"Bot detected on page {i} (URL: {page.url()})")
                    break

                # Get items
                items = page.locator('div[data-component-type="s-search-result"]').all()
                print(f"Found {len(items)} items on page {i}")
                
                for item in items:
                    try:
                        name = item.locator('h2 a span').first.inner_text()
                        
                        price_locator = item.locator('.a-price-whole').first
                        if price_locator.count() > 0:
                            price_text = price_locator.inner_text().replace(',', '').replace('\n', '').strip()
                            price = int(price_text) if price_text.isdigit() else 0
                        else:
                            price = 0
                            
                        rating_locator = item.locator('.a-icon-alt').first
                        rating = rating_locator.inner_text() if rating_locator.count() > 0 else "N/A"
                        
                        reviews_locator = item.locator('.a-size-base.s-underline-text').first
                        if reviews_locator.count() > 0:
                            reviews_text = reviews_locator.inner_text().replace('(', '').replace(')', '').replace(',', '').strip()
                            reviews = int(reviews_text) if reviews_text.isdigit() else 0
                        else:
                            reviews = 0
                            
                        products.append({
                            "name": name,
                            "price": price,
                            "rating": rating,
                            "reviews": reviews,
                            "page": i
                        })
                    except Exception:
                        continue
                        
            except Exception as e:
                print(f"Error navigating to page {i}: {e}")
                break
                
        browser.close()
        
        with open('jbl_products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
            
        return products

if __name__ == "__main__":
    results = scrape_amazon_jbl()
    print(f"Successfully scraped {len(results)} products.")
