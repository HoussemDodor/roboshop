import sys
import os
import json
import streamlit as st

# Make 'agents/' importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.branding_engine import generate_branding, save_product_with_branding
from agents.product_research_engine import generate_product_ideas

# --- Config ---
st.set_page_config(page_title="RoboShop Dashboard", layout="wide")
st.title("RoboShop Product Ideas")

# --- Button to refresh the products
if st.button("🔁 Generate New Product Ideas"):
    with st.spinner("Thinking up some trending desk accessories..."):
        success, result = generate_product_ideas()
        if success:
            st.success("Product ideas generated successfully. Refreshing dashboard...")
            st.rerun()
        else:
            st.error(f"Failed to generate ideas: {result}")

PRODUCT_FILE = "data/product_ideas.json"
SAVED_PRODUCTS_DIR = "data/products"
os.makedirs(SAVED_PRODUCTS_DIR, exist_ok=True)

# --- Helper to display branding ---
def display_branding(product, branding):
    with st.expander("📦 Branding Preview", expanded=True):
        st.write(f"**Product Title:** {branding.get('product_title', '')}")
        st.write(f"**Short Description:** {branding.get('short_description', '')}")
        st.write(f"**Long Description:** {branding.get('long_description', '')}")
        st.write("**Unique Selling Points:**")
        for usp in branding.get("unique_selling_points", []):
            st.markdown(f"- {usp}")
        st.write(f"**Instagram Caption:** {branding.get('instagram_caption', '')}")
        st.write(f"**Hashtags:** `{', '.join(branding.get('suggested_hashtags', []))}`")
        st.write(f"**Brand Tone:** {branding.get('brand_tone', '')}")


# --- Section: Product Ideas ---
st.header("🛍️ Product Ideas")

if not os.path.exists(PRODUCT_FILE):
    st.warning("No product ideas found. Please run the product researcher agent.")
else:
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        product_data = json.load(f)
        ideas = product_data.get("products", [])

    if not ideas:
        st.warning("No valid product entries found.")
    else:
        for i, item in enumerate(ideas):
            if not isinstance(item, dict):
                st.error(f"⚠️ Product {i+1} is malformed or not a dictionary.")
                st.code(repr(item))
                continue
            
            with st.container():
                st.subheader(f"{i + 1}. {item.get('product_name', 'Unnamed Product')}")
                st.write(f"**Description:** {item.get('description', 'N/A')}")
                st.write(f"**Why It Appeals:** {item.get('target_audience_appeal', 'N/A')}")
                st.write(f"**Keywords:** `{', '.join(item.get('keywords', []))}`")

                brand_key = f"branding_{i}"
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("✨ Generate Branding", key=f"gen_btn_{i}"):
                        try:
                            with st.spinner("Generating..."):
                                branding = generate_branding(item)
                                st.session_state[brand_key] = branding
                                st.success("Branding generated!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

                with col2:
                    if brand_key in st.session_state:
                        branding = st.session_state[brand_key]
                        if st.button("💾 Save Product", key=f"save_btn_{i}"):
                            path = save_product_with_branding(item, branding)
                            st.success(f"Saved to: {path}")

                if brand_key in st.session_state:
                    display_branding(item, st.session_state[brand_key])

                st.markdown("---")


# --- Section: View Saved Products ---
st.header("📂 View Saved Products")

saved_files = [f for f in os.listdir(SAVED_PRODUCTS_DIR) if f.endswith(".json")]

if not saved_files:
    st.info("No saved products found.")
else:
    selected_file = st.selectbox("Select a saved product file:", saved_files)

    if selected_file:
        file_path = os.path.join(SAVED_PRODUCTS_DIR, selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        product = data.get("product", {})
        branding = data.get("branding", {})

        st.subheader(f"🛍️ {branding.get('product_title', product.get('product_name', 'Unnamed Product'))}")
        st.caption(f"File: `{selected_file}`")
        st.write(f"**Description:** {product.get('description', '')}")
        st.write(f"**Why It Appeals:** {product.get('target_audience_appeal', '')}")
        st.write(f"**Keywords:** `{', '.join(product.get('keywords', []))}`")

        display_branding(product, branding)
