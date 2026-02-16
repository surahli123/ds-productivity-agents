#!/usr/bin/env python3
"""
Fetch Medium and tech blog articles and save them as markdown.
Uses Playwright for browser automation to bypass anti-scraping measures.
"""

import asyncio
from playwright.async_api import async_playwright
import html2text
import os
import re

# List of articles to fetch (Netflix already downloaded)
ARTICLES = [
    {
        "url": "https://medium.com/udemy-engineering/evolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364",
        "filename": "udemy-ai-intent-understanding.md"
    },
    {
        "url": "https://medium.com/airbnb-engineering/how-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5",
        "filename": "airbnb-future-value-tradeoffs.md"
    },
    {
        "url": "https://medium.com/airbnb-engineering/discovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c",
        "filename": "airbnb-message-intent-classification.md"
    },
    {
        "url": "https://medium.com/airbnb-engineering/how-airbnb-measures-listing-lifetime-value-a603bf05142c",
        "filename": "airbnb-listing-lifetime-value.md"
    }
]

OUTPUT_DIR = "dev/test-fixtures"


def clean_markdown(text):
    """Clean up the markdown text."""
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


async def fetch_article(url, filename):
    """Fetch a single article and save as markdown."""
    print(f"Fetching: {url}")

    async with async_playwright() as p:
        # Launch browser with more realistic settings to avoid detection
        browser = await p.chromium.launch(
            headless=False,  # Use headed mode (some sites detect headless)
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        # Create context with realistic user agent and viewport
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US'
        )

        page = await context.new_page()

        try:
            # Navigate with a more lenient wait condition
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Wait longer for the article content to appear
            # Try to wait for article content specifically
            try:
                await page.wait_for_selector('article, .article, [role="main"]', timeout=20000)
            except:
                print(f"  Warning: Couldn't find article selector, continuing anyway...")

            # Additional wait for dynamic content
            await page.wait_for_timeout(5000)

            # Get the page content
            content = await page.content()

            # Convert HTML to Markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.ignore_emphasis = False
            h.body_width = 0  # Don't wrap lines

            markdown = h.handle(content)
            markdown = clean_markdown(markdown)

            # Save to file
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Source: {url}\n\n")
                f.write(markdown)

            print(f"✓ Saved to: {output_path}")

        except Exception as e:
            print(f"✗ Error fetching {url}: {e}")

        finally:
            await browser.close()


async def main():
    """Fetch all articles."""
    print(f"Fetching {len(ARTICLES)} articles...\n")

    # Fetch articles one at a time to avoid rate limiting
    for article in ARTICLES:
        await fetch_article(article["url"], article["filename"])
        # Wait between requests to be polite
        await asyncio.sleep(2)

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
