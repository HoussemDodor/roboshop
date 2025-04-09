# frontend/dashboard.py

import streamlit as st
import json
import os

st.set_page_config(page_title="RoboShop Dashboard", layout="wide")
st.title("RoboShop Product Ideas")

file_path = "data/product_ideas.json"

if not os.path.exists(file_path):
    st.warning("No product ideas found. Please run the product researcher agent first.")
else:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        ideas = data.get("products", [])

    if not ideas:
        st.warning("No valid product entries found.")
    else:
        for i, item in enumerate(ideas):
            with st.container():
                st.subheader(f"{i+1}. {item.get('product_name', 'Unnamed Product')}")
                st.write(f"**Description:** {item.get('description', 'N/A')}")
                st.write(f"**Why It Appeals:** {item.get('target_audience_appeal', 'N/A')}")
                st.write(f"**Keywords:** `{', '.join(item.get('keywords', []))}`")
                st.markdown("---")
