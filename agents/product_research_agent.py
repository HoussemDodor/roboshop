# agents/product_research_agent.py

import json
from dotenv import load_dotenv
import os
import re
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
Each idea should include the following fields using **snake_case JSON keys only**:
- product_name
- description
- target_audience_appeal
- keywords (3–5 relevant search terms)

{NICHE_INFO}

Return the result in raw JSON format only.
Do NOT include any explanations, commentary, or markdown formatting.
Do NOT wrap the response in triple backticks or label it as a code block.

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
    # Clean triple backticks if present
    cleaned_text = re.sub(r"```json|```", "", text).strip()

    try:
        ideas = json.loads(cleaned_text)
        product_data = {"products": ideas}
        os.makedirs("data", exist_ok=True)
        with open("data/product_ideas.json", "w", encoding="utf-8") as f:
            json.dump(product_data, f, indent=4)
        print("Product ideas saved to data/product_ideas.json")
        return product_data
    except json.JSONDecodeError:
        print("Failed to parse cleaned response as JSON:")
        print(cleaned_text)
    return None

if __name__ == "__main__":
    get_product_ideas()
