# frontend/dashboard.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from agents.branding_engine import generate_branding, save_product_with_branding
import json

st.set_page_config(page_title="RoboShop Dashboard", layout="wide")
st.title("RoboShop Product Ideas")

# --- Load Product Ideas ---
product_file = "data/product_ideas.json"

st.header("🛍️ Product Ideas")
if not os.path.exists(product_file):
    st.warning("No product ideas found. Please run the product researcher agent.")
else:
    with open(product_file, "r", encoding="utf-8") as f:
        product_data = json.load(f)
        ideas = product_data.get("products", [])

    if not ideas:
        st.warning("No valid product entries found.")
    else:
        for i, item in enumerate(ideas):
            with st.container():
                st.subheader(f"{i + 1}. {item.get('product_name', 'Unnamed Product')}")
                st.write(f"**Description:** {item.get('description', 'N/A')}")
                st.write(f"**Why It Appeals:** {item.get('target_audience_appeal', 'N/A')}")
                st.write(f"**Keywords:** `{', '.join(item.get('keywords', []))}`")

                # Unique key for each product
                brand_key = f"branding_{i}"

                # Generate Branding Button
                if st.button(f"Generate Branding for Product {i + 1}", key=f"gen_btn_{i}"):
                    with st.spinner("Generating branding..."):
                        branding = generate_branding(item)
                        st.session_state[brand_key] = branding
                        st.success("Branding generated!")

                # Show branding if it exists in session state
                if brand_key in st.session_state:
                    branding = st.session_state[brand_key]

                    st.write(f"**Product Title:** {branding.get('product_title', '')}")
                    st.write(f"**Short Description:** {branding.get('short_description', '')}")
                    st.write(f"**Long Description:** {branding.get('long_description', '')}")
                    st.write("**Unique Selling Points:**")
                    for usp in branding.get("unique_selling_points", []):
                        st.markdown(f"- {usp}")
                    st.write(f"**Instagram Caption:** {branding.get('instagram_caption', '')}")
                    st.write(f"**Hashtags:** `{', '.join(branding.get('suggested_hashtags', []))}`")
                    st.write(f"**Brand Tone:** {branding.get('brand_tone', '')}")

                    # Save button
                    if st.button(f"💾 Save Product", key=f"save_btn_{i}"):
                        path = save_product_with_branding(item, branding)
                        st.success(f"Saved to {path}")
                st.markdown("---")

st.markdown("---")

st.header("📂 View Saved Products")

products_dir = "data/products"
if not os.path.exists(products_dir):
    os.makedirs(products_dir)

saved_files = [f for f in os.listdir(products_dir) if f.endswith(".json")]

if not saved_files:
    st.info("No saved products found.")
else:
    selected_file = st.selectbox("Select a saved product file:", saved_files)

    if selected_file:
        file_path = os.path.join(products_dir, selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        product = data.get("product", {})
        branding = data.get("branding", {})

        st.subheader(f"🛍️ {branding.get('product_title', product.get('product_name', 'Unnamed Product'))}")
        st.write(f"**Description:** {product.get('description', '')}")
        st.write(f"**Why It Appeals:** {product.get('target_audience_appeal', '')}")
        st.write(f"**Keywords:** `{', '.join(product.get('keywords', []))}`")

        st.write("### Branding Content")
        st.write(f"**Short Description:** {branding.get('short_description', '')}")
        st.write(f"**Long Description:** {branding.get('long_description', '')}")
        st.write("**Unique Selling Points:**")
        for usp in branding.get("unique_selling_points", []):
            st.markdown(f"- {usp}")
        st.write(f"**Instagram Caption:** {branding.get('instagram_caption', '')}")
        st.write(f"**Hashtags:** `{', '.join(branding.get('suggested_hashtags', []))}`")
        st.write(f"**Brand Tone:** {branding.get('brand_tone', '')}")