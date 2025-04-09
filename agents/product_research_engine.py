import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

HISTORY_FILE = "data/idea_history.json"
OUTPUT_FILE = "data/product_ideas.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(all_ideas):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_ideas, f, indent=4)

def get_exclusion_list(history):
    names = [idea["product_name"].lower() for idea in history]
    return list(set(names))


NICHE_FILE = "niche.txt"

def load_niche():
    if not os.path.exists(NICHE_FILE):
        raise FileNotFoundError("niche.txt not found. Please define your niche first.")
    with open(NICHE_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(excluded_names):
    niche_info = load_niche()
    excluded_text = ", ".join([f'"{name}"' for name in excluded_names[:20]])  # Limit size

    return f"""
You are a product research assistant specializing in e-commerce niches.

Your task is to generate five **real, currently trending** product ideas based on the following niche information.

{niche_info}

Avoid suggesting any products named: {excluded_text}

Requirements:
- ONLY suggest product ideas that reflect real, trending, or commonly searched items on platforms like Amazon, Etsy, Google Trends, or TikTok Shop.
- Avoid fictional, overly imaginative, or non-existent product types.
- Use short, commercially-viable product names (as seen in real listings)
- Use snake_case keys only.
- Output raw JSON only — no markdown, no triple backticks, no commentary.

Return the result in raw JSON format only.
Do NOT include any explanations, commentary, or markdown formatting.
Do NOT wrap the response in triple backticks or label it as a code block.

Each product should be structured as a JSON object with the following keys:
- product_name: Full product name including qualifiers
- description: 1–2 sentence overview of the product’s function and appeal
- target_audience_appeal: Why this product would appeal to the target audience
- keywords: 3–5 search terms relevant to the product
"""



def generate_product_ideas(output_path=OUTPUT_FILE):
    history = load_history()
    excluded_names = get_exclusion_list(history)
    prompt = build_prompt(excluded_names)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    text = response.choices[0].message.content
    import ast

    cleaned_text = re.sub(r"```json|```", "", text).strip()

    try:
        # Try loading as JSON first
        new_ideas = json.loads(cleaned_text)

    except json.JSONDecodeError:
        try:
            # Attempt to handle single-quoted strings with ast.literal_eval
            parsed = ast.literal_eval(cleaned_text)

            if isinstance(parsed, list):
                new_ideas = parsed
            else:
                raise ValueError("Model response is not a list.")
        except Exception as e:
            return False, f"Failed to parse model response: {str(e)}"

    # Final validation
    if not isinstance(new_ideas, list) or not all(isinstance(i, dict) for i in new_ideas):
        return False, "Parsed response is not a list of product dictionaries."

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"products": new_ideas}, f, indent=4)

    # Save to history
    updated_history = load_history() + new_ideas
    save_history(updated_history)

    return True, new_ideas

