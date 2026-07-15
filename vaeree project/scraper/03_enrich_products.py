from playwright.sync_api import sync_playwright
import pandas as pd

from helpers import safe_text, get_detail, get_seller

# Read previous CSV
df = pd.read_csv("data/products_detailed.csv")

colors = []
materials = []
spaces = []
sellers = []
ratings = []
reviews = []
current_prices = []
original_prices = []
discounts = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for index, row in df.iterrows():

        print(f"Scraping {index + 1}/{len(df)}")

        page.goto(row["URL"])

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # -----------------------------
        # Product Details
        # -----------------------------

        color = get_detail(page, "Color")
        material = get_detail(page, "Material")
        space = get_detail(page, "Space")
        seller = get_seller(page)

        # -----------------------------
        # Ratings
        # -----------------------------

        rating = safe_text(
            page.locator(".reviews-summary-rating p")
        )

        review_count = safe_text(
            page.locator(".reviews-summary-rating-copy span").nth(1)
        )

        # -----------------------------
        # Current Price
        # -----------------------------

        current_price = safe_text(
            page.locator("p.pdp-price-value")
        )

        current_price = (
            current_price.replace("₹", "")
                         .replace(",", "")
                         .replace("â‚¹", "")
                         .strip()
        )

        # -----------------------------
        # Original Price (MRP)
        # -----------------------------

        original_price = safe_text(
            page.locator("p.pdp-price-compare")
        )

        original_price = (
            original_price.replace("MRP", "")
                          .replace("₹", "")
                          .replace(",", "")
                          .replace("â‚¹", "")
                          .strip()
        )

        # -----------------------------
        # Discount %
        # -----------------------------

        discount = safe_text(
            page.locator("p.pdp-price-discount")
        )

        discount = (
            discount.replace("% OFF", "")
                    .replace("%", "")
                    .replace("OFF", "")
                    .strip()
        )

        # Handle products without discounts

        if current_price == "":
            current_price = row["Price"]

        if original_price == "":
            original_price = current_price

        if discount == "":
            discount = 0

        # -----------------------------
        # Store Values
        # -----------------------------

        colors.append(color)
        materials.append(material)
        spaces.append(space)
        sellers.append(seller)
        ratings.append(rating)
        reviews.append(review_count)

        current_prices.append(current_price)
        original_prices.append(original_price)
        discounts.append(discount)

    browser.close()

# -----------------------------
# Add columns
# -----------------------------

df["Price"] = current_prices
df["Original Price"] = original_prices
df["Discount %"] = discounts

df["Color"] = colors
df["Material"] = materials
df["Space"] = spaces
df["Seller"] = sellers
df["Rating"] = ratings
df["Reviews"] = reviews

# -----------------------------
# Save
# -----------------------------

df.to_csv(
    "data/master_products.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(f"\nTotal Products: {len(df)}")
print("\nMaster dataset created successfully!")