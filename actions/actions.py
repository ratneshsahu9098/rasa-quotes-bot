import csv
import random
import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Global dictionary to hold categorized quotes
QUOTES_DB = {}
CSV_PATH = r"C:\Project\actions\quotes.csv"

# Map rasa intents to keywords we expect in the dataset's 'category' column
INTENT_CATEGORY_MAP = {
    "mood_unhappy": ["sad", "heartbreak", "loss", "pain", "death", "lonely", "grief"],
    "mood_great": ["happiness", "joy", "smile", "positive", "perfect", "good"],
    "mood_love": ["love", "romance", "kiss", "relationships", "marriage"],
    "mood_life": ["life", "living", "reality", "experience", "growing"],
    "mood_inspiration": ["inspiration", "inspirational", "hope", "courage", "strength", "motivational", "success"],
    "mood_funny": ["humor", "funny", "joke", "comedy", "laugh"]
}

def load_quotes():
    """Load quotes from the CSV dataset into memory."""
    if not os.path.exists(CSV_PATH):
        print(f"Warning: Dataset not found at {CSV_PATH}. Using fallback quotes.")
        return

    print("Loading quotes dataset (this may take a few moments)...")
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                quote_text = row.get("quote", "").strip()
                author = row.get("author", "Unknown").strip()
                categories_str = row.get("category", "")
                
                if not quote_text:
                    continue
                
                # Clean up quotes that might be entirely wrapped in outer quotes
                if quote_text.startswith('"') and quote_text.endswith('"'):
                    quote_text = quote_text[1:-1]
                
                full_quote = f"{quote_text} - {author}"
                
                # Split categories and map to generic groups based on our INTENT_CATEGORY_MAP keys
                found_match = False
                for cat in [c.strip().lower() for c in categories_str.split(",")]:
                    for intent, keywords in INTENT_CATEGORY_MAP.items():
                        if cat in keywords:
                            if intent not in QUOTES_DB:
                                QUOTES_DB[intent] = []
                            QUOTES_DB[intent].append(full_quote)
                            found_match = True
                            
                # If no specific category matched, put it in 'general'
                if not found_match:
                    if "general" not in QUOTES_DB:
                        QUOTES_DB["general"] = []
                    QUOTES_DB["general"].append(full_quote)
                    
        print(f"Loaded quotes into {len(QUOTES_DB)} categories.")
        for k, v in QUOTES_DB.items():
            print(f"  - {k}: {len(v)} quotes")
    except Exception as e:
        print(f"Error loading CSV: {e}")

# Load the dataset ONCE when the actions server starts up
load_quotes()

# Fallback basic quotes in case the dataset fails to load or is completely empty
FALLBACK_QUOTES = {
    "mood_unhappy": ["The way to get started is to quit talking and begin doing. - Walt Disney"],
    "mood_great": ["Tell me and I forget. Teach me and I remember. Involve me and I learn. - Benjamin Franklin"],
    "mood_love": ["Love all, trust a few, do wrong to none. - William Shakespeare"],
    "mood_life": ["Life is what happens when you're busy making other plans. - John Lennon"],
    "mood_inspiration": ["The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"],
    "mood_funny": ["I am so clever that sometimes I don't understand a single word of what I am saying. - Oscar Wilde"],
    "general": ["You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. - Dr. Seuss"]
}

class ActionRecommendQuote(Action):

    def name(self) -> Text:
        return "action_recommend_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the user's latest intent to determine mood/sentiment
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        # Decide which dictionary to query
        db_to_use = QUOTES_DB if QUOTES_DB else FALLBACK_QUOTES
        
        if intent in db_to_use and db_to_use[intent]:
            category = intent
        else:
            category = "general"
            
        quotes_list = db_to_use.get(category, db_to_use.get("general", ["No quotes found!"]))
        selected_quote = random.choice(quotes_list)

        dispatcher.utter_message(text=f"Here is a quote for you:\n\n\"{selected_quote}\"")

        return []
