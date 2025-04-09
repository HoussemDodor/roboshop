# agents/branding_engine.py

import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_branding(product: dict) -> dict:
    prompt = f"""
You are a branding and marketing assistant for an online store that specializes in minimalist desk accessories.

Using the following product details, generate structured branding content.

Product Name: {product['product_name']}
Description: {product['description']}
Target Appeal: {product['target_audience_appeal']}
Keywords: {', '.join(product['keywords'])}

Return the result as raw JSON only.
Do NOT include markdown formatting or triple backticks.

Required keys:
- product_title
- short_description
- long_description
- unique_selling_points (list of 3–5)
- instagram_caption
- suggested_hashtags
- brand_tone
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw = response.choices[0].message.content
    cleaned = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        raise ValueError("Failed to parse branding response:\n" + cleaned)
    

def save_product_with_branding(product: dict, branding: dict, directory="data/products"):
    # Combine data
    combined = {
        "product": product,
        "branding": branding
    }

    # Create a slug for the filename
    name = branding.get("product_title", product.get("product_name", "product")).lower()
    slug = name.replace(" ", "_").replace("-", "_")
    filename = f"{slug}.json"

    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)

    return file_path