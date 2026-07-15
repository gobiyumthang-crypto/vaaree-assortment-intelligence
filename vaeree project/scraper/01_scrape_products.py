from playwright.sync_api import sync_playwright
import pandas as pd

# Store all products here
all_products = []

with sync_playwright() as p:

    # Open browser
    browser = p.chromium.launch(headless=False)

    # Open new page
    page = browser.new_page()

    # Loop through all 3 pages
    for page_number in range(1, 4):

        url = f"https://vaaree.com/collections/dustbins?page={page_number}"

        print(f"Scraping Page {page_number}...")

        page.goto(url)

        page.wait_for_timeout(3000)

        # Find all elements
        titles = page.locator("p.sf-product-card-title")
        subtitles = page.locator("p.sf-product-card-subtitle")
        prices = page.locator("p.sf-product-card-price")
        links = page.locator("a.sf-product-card-copy")

        count = titles.count()

        # Loop through every product on the page
        for i in range(count):

            product = {
                "Product Name": titles.nth(i).inner_text() + " " + subtitles.nth(i).inner_text(),
                "Price": prices.nth(i).inner_text().replace("₹", "").replace(",", "").replace("â‚¹", "").strip(),
                "URL": "https://vaaree.com" + links.nth(i).get_attribute("href")
            }

            all_products.append(product)

    browser.close()

# Convert to DataFrame
df = pd.DataFrame(all_products)

# Save CSV
df.to_csv("data/products.csv", index=False, encoding="utf-8-sig")

# Print first 5 products
print(df.head())

# Print total products
print(f"\nTotal Products Scraped: {len(df)}")

print("\nCSV saved successfully to data/products.csv")