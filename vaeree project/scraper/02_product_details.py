from playwright.sync_api import sync_playwright
import pandas as pd

# Read the products CSV
df = pd.read_csv("data/products.csv")

stock_status = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for index, row in df.iterrows():

        print(f"Checking {index + 1}/{len(df)}")

        page.goto(row["URL"])

        # Wait for the page to load
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)

        # Look for the OUT OF STOCK button
        out_of_stock_button = page.locator("button.pdp-out-of-stock-cta")

        if out_of_stock_button.count() > 0:
            stock_status.append("Out of Stock")
        else:
            stock_status.append("In Stock")

    browser.close()

# Add stock status to dataframe
df["Stock Status"] = stock_status

# Save updated CSV
df.to_csv(
    "data/products_detailed.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(f"\nTotal Products: {len(df)}")
print("\nDone! CSV saved as data/products_detailed.csv")