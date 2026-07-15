import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Vaaree Assortment Intelligence",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------

df = pd.read_csv("data/master_products.csv")

# Clean numeric columns
for col in ["Price", "Original Price", "Discount %"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.title("Filters")

materials = sorted(df["Material"].dropna().unique())
selected_material = st.sidebar.multiselect(
    "Material",
    materials,
    default=materials
)

sellers = sorted(df["Seller"].dropna().unique())
selected_seller = st.sidebar.multiselect(
    "Seller",
    sellers,
    default=sellers
)

stock = st.sidebar.multiselect(
    "Stock Status",
    df["Stock Status"].unique(),
    default=df["Stock Status"].unique()
)

filtered = df[
    (df["Material"].isin(selected_material))
    &
    (df["Seller"].isin(selected_seller))
    &
    (df["Stock Status"].isin(stock))
]

# -----------------------------
# KPIs
# -----------------------------

st.title("📊 Vaaree Assortment Intelligence Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Products", len(filtered))
c2.metric("In Stock", (filtered["Stock Status"] == "In Stock").sum())
c3.metric("Out of Stock", (filtered["Stock Status"] == "Out of Stock").sum())
c4.metric("Average Price", f"₹{filtered['Price'].mean():.0f}")
c5.metric("Average Discount", f"{filtered['Discount %'].mean():.0f}%")

st.divider()

# -----------------------------
# Charts
# -----------------------------

left, right = st.columns(2)

with left:

    st.subheader("Price Distribution")

    fig = px.histogram(
        filtered,
        x="Price",
        nbins=20
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("Material Mix")

    fig = px.pie(
        filtered,
        names="Material"
    )

    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:

    st.subheader("Stock Status")

    fig = px.pie(
        filtered,
        names="Stock Status",
        hole=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("Top Sellers")

    seller_counts = (
        filtered["Seller"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    seller_counts.columns = ["Seller", "Products"]

    fig = px.bar(
        seller_counts,
        x="Seller",
        y="Products"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# AI Insights
# -----------------------------

st.divider()

st.subheader("📈 Category Insights")

plastic_share = (
    (filtered["Material"] == "Plastic").sum()
    / len(filtered)
    * 100
)

out_stock = (
    (filtered["Stock Status"] == "Out of Stock").sum()
    / len(filtered)
    * 100
)

top_seller = filtered["Seller"].value_counts().idxmax()

st.success(
f"""
• Total assortment contains **{len(filtered)} products**

• **{plastic_share:.0f}%** of the assortment is Plastic.

• **{out_stock:.0f}%** of products are Out of Stock.

• Largest seller is **{top_seller}**.

• Average selling price is **₹{filtered['Price'].mean():.0f}**.

• Average discount offered is **{filtered['Discount %'].mean():.0f}%**.
"""
)

# -----------------------------
# Product Table
# -----------------------------

st.divider()

st.subheader("Products")

st.dataframe(
    filtered,
    use_container_width=True
)
