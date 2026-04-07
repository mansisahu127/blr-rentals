import asyncio
import hashlib
from playwright.async_api import async_playwright
from app.services.ingestion import ingest_listing

async def scrape_nobroker():
    # Targeted high-demand areas in Bengaluru
    localities = ["hsr-layout", "whitefield", "koramangala", "indiranagar"]
    
    print("🚀 Starting NoBroker Targeted Scraper...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for area in localities:
            # Added 'sort=last_updated_desc' to get the freshest posts
            url = f"https://www.nobroker.in/flats-for-rent-in-{area}_bangalore?sort=last_updated_desc"
            print(f"🔍 Scraping {area}...")

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(4) # Wait for JS rendering
                
                # Scroll once to reveal the first batch of cards
                await page.mouse.wheel(0, 1500)
                await asyncio.sleep(2)

                # Find the listing cards
                listings = await page.query_selector_all("article, [id^='property-']")
                
                # Limit to top 10 recent listings per area for minimal compute
                recent_listings = listings[:10] 
                print(f"✅ Found {len(recent_listings)} recent listings in {area}")

                for card in recent_listings:
                    raw_text = await card.inner_text()
                    normalized = " ".join(raw_text.split())

                    # Deterministic ID from area + content — same listing deduplicates,
                    # different listings (even at the same DOM position) stay unique
                    content_hash = hashlib.sha256(f"{area}:{normalized}".encode()).hexdigest()[:16]
                    source_id = f"nb-{area}-{content_hash}"

                    ingest_listing(normalized, "nobroker", source_id)

            except Exception as e:
                print(f"Failed to scrape {area}: {e}")
                continue 

        await browser.close()
        print("Targeted Scrape Complete.")