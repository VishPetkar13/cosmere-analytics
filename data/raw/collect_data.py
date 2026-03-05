# ─────────────────────────────────────────────────────────
# COSMERE ANALYTICS — Data Collection Script
# Uses the Hardcover GraphQL API to fetch book data
# ─────────────────────────────────────────────────────────

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HARDCOVER_API_KEY")

API_URL = "https://api.hardcover.app/v1/graphql"


books = [
    # --- Mistborn Era 1 ---
    {"search_title": "Mistborn The Final Empire Brandon Sanderson",       "series": "Mistborn Era 1",     "series_order": 1},
    {"search_title": "The Well of Ascension Brandon Sanderson",           "series": "Mistborn Era 1",     "series_order": 2},
    {"search_title": "The Hero of Ages Brandon Sanderson",                "series": "Mistborn Era 1",     "series_order": 3},

    # --- Mistborn Era 2 ---
    {"search_title": "The Alloy of Law Brandon Sanderson",                "series": "Mistborn Era 2",     "series_order": 1},
    {"search_title": "Shadows of Self Brandon Sanderson",                 "series": "Mistborn Era 2",     "series_order": 2},
    {"search_title": "The Bands of Mourning Brandon Sanderson",           "series": "Mistborn Era 2",     "series_order": 3},
    {"search_title": "The Lost Metal Brandon Sanderson",                  "series": "Mistborn Era 2",     "series_order": 4},

    # --- Stormlight Archive ---
    {"search_title": "The Way of Kings Brandon Sanderson",                "series": "Stormlight Archive", "series_order": 1},
    {"search_title": "Words of Radiance Brandon Sanderson",               "series": "Stormlight Archive", "series_order": 2},
    {"search_title": "Oathbringer Brandon Sanderson",                     "series": "Stormlight Archive", "series_order": 3},
    {"search_title": "Rhythm of War Brandon Sanderson",                   "series": "Stormlight Archive", "series_order": 4},
    {"search_title": "Wind and Truth Brandon Sanderson",                  "series": "Stormlight Archive", "series_order": 5},

    # --- Elantris ---
    {"search_title": "Elantris Brandon Sanderson",                        "series": "Elantris",           "series_order": 1},
    {"search_title": "The Hope of Elantris Brandon Sanderson",            "series": "Elantris",           "series_order": 2},

    # --- Warbreaker ---
    {"search_title": "Warbreaker Brandon Sanderson",                      "series": "Warbreaker",         "series_order": 1},

    # --- Standalone Cosmere ---
    {"search_title": "The Emperor's Soul Brandon Sanderson",              "series": "Standalone",         "series_order": 1},
    {"search_title": "Tress of the Emerald Sea Brandon Sanderson",        "series": "Standalone",         "series_order": 2},
    {"search_title": "Yumi and the Nightmare Painter Brandon Sanderson",  "series": "Standalone",         "series_order": 3},
    {"search_title": "The Sunlit Man Brandon Sanderson",                  "series": "Standalone",         "series_order": 4},
]


QUERY = """
query SearchBook {
  search(query: "%s", query_type: "Book", per_page: 1) {
    results
  }
}
"""

def fetch_book(search_title):
    # Build the headers — this is where Bearer + API key goes
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    # Insert the book title into the query template
    query = QUERY % search_title

    try:
        # Send the POST request to the API
        response = requests.post(
            API_URL,
            json={"query": query},
            headers=headers,
            timeout=10
        )

        # Parse the JSON response
        data = response.json()

        # Navigate into the nested response to find the hits
        hits = data["data"]["search"]["results"]["hits"]

        # If we got at least one result back, return the first one
        if hits:
            return hits[0]["document"]

    except Exception as e:
        print(f"   Error fetching '{search_title}': {e}")

    return None

all_books = []

for book in books:
    print(f"📖 Fetching: {book['search_title']}...")

    result = fetch_book(book["search_title"])

    if result:
        row = {
            "title":              result.get("title"),
            "series":             book["series"],
            "series_order":       book["series_order"],
            "hardcover_id":       result.get("id"),
            "release_year":       result.get("release_year"),
            "pages":              result.get("pages"),
            "rating":             result.get("rating"),
            "ratings_count":      result.get("ratings_count"),
            "reviews_count":      result.get("reviews_count"),
            "users_read_count":   result.get("users_read_count"),
            "has_audiobook":      result.get("has_audiobook"),
            "has_ebook":          result.get("has_ebook"),
            "genres":             "|".join(result.get("genres", [])),
            "moods":              "|".join(result.get("moods", [])),
            "content_warnings":   "|".join(result.get("content_warnings", [])),
            "description":        result.get("description"),
        }

        all_books.append(row)
        print(f"   Found: {result.get('title')} (rating: {result.get('rating')})")

    else:
        print(f"   No result found for: {book['search_title']}")

    time.sleep(1)

    df = pd.DataFrame(all_books)
df.to_csv("data/raw/cosmere_books.csv", index=False)

print(f"\n Done! {len(df)} books saved to data/raw/cosmere_books.csv")
print("\n--- Preview ---")
print(df[["title", "series", "rating", "ratings_count", "pages"]].to_string())