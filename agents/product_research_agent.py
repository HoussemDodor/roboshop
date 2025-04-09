# agents/product_research_agent.py

import json
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

NICHE_INFO = """
Niche: Desk Accessories

Focus: Modern, minimalist products for remote workers and digital creatives

Target Audience:
- Age 25–40
- Works from home or in co-working spaces
- Prefers a clean, aesthetic, and organized desk
- Shops online and values design-forward solutions

Keywords: desk organization, cable management, minimal design, productivity tools, home office decor
"""

PROMPT = f"""
You are a product research assistant specializing in e-commerce niches.

Based on the following niche and audience, generate 5 trending product ideas.
For each, include:
1. Product Name
2. Description (2–3 sentences)
3. Why this would appeal to the target audience
4. 3–5 relevant keywords

{NICHE_INFO}

Respond in JSON format as a list of product objects.
"""

def get_product_ideas():
    print("Generating product ideas for desk accessories...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.7
    )

    text = response.choices[0].message.content

    try:
        product_data = json.loads(text)
        os.makedirs("data", exist_ok=True)
        with open("data/product_ideas.json", "w", encoding="utf-8") as f:
            json.dump(product_data, f, indent=4)
        print("Product ideas saved to data/product_ideas.json")
        return product_data
    except json.JSONDecodeError:
        print("Failed to parse response as JSON. Here's what was returned:\n")
        print(text)
        return None

if __name__ == "__main__":
    get_product_ideas()
