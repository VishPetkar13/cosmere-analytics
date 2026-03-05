# ─────────────────────────────────────────────────────────
# COSMERE ANALYTICS — Fix Problem Books Script
#
# Our main collect_data.py fetched wrong results for 5 books
# because the search API returned summaries/reviews instead
# of the actual novels. 
#
# This script fetches those 5 books directly by their 
# Hardcover ID — which is 100% precise, no ambiguity.
# Then it patches the main CSV replacing the wrong rows.
# ─────────────────────────────────────────────────────────

import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("HARDCOVER_API_KEY")
print("API KEY LOADED:", API_KEY[:20] if API_KEY else "NOT FOUND")
API_URL = "https://api.hardcover.app/v1/graphql"

problem_books = [
    {"id": 427863, "series": "Mistborn Era 2",     "series_order": 4},
    {"id": 386446, "series": "Stormlight Archive", "series_order": 1},
    {"id": 374131, "series": "Stormlight Archive", "series_order": 2},
    {"id": 338931, "series": "Elantris",           "series_order": 1},
    {"id": 385491, "series": "Warbreaker",         "series_order": 1},
]

# This is different from our search query.
# Instead of searching by title, we ask for one
# specific book using its exact numeric ID.
QUERY = """
query GetBookById {
  books(where: {id: {_eq: %d}}) {
    id
    title
    rating
    ratings_count
    reviews_count
    pages
    release_year
    description
    users_read_count
    default_audio_edition_id
    default_ebook_edition_id
    taggings {
      taggable_type
      tag {
        tag
        tag_category {
          category
        }
      }
    }
  }
}
"""

def fetch_by_id(book_id):
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    query = QUERY % book_id

    try:
        response = requests.post(
            API_URL,
            json={"query": query},
            headers=headers,
            timeout=10
        )

        data = response.json()
        
        # The response structure is different from search —
        # it returns a 'books' array directly instead of 'hits'
        books = data["data"]["books"]

        if books:
            return books[0]

    except Exception as e:
        print(f"   Error fetching ID {book_id}: {e}")

    return None


fixed_rows = []

for book in problem_books:
    print(f" Fetching ID {book['id']}...")

    result = fetch_by_id(book["id"])

    if result:
        # taggings contains genres, moods and content warnings all mixed together
        # Each tagging has a 'taggable_type' telling us which category it belongs to
        # We filter by taggable_type to separate them out
        taggings = result.get("taggings", [])

        # Use sets to automatically remove duplicates
        # Note: category is "Content Warning" with a space, not "ContentWarning"
        genres   = "|".join(sorted(set([
            t["tag"]["tag"] for t in taggings
            if t.get("tag") and t["tag"].get("tag_category")
            and t["tag"]["tag_category"].get("category") == "Genre"
        ])))
        moods    = "|".join(sorted(set([
            t["tag"]["tag"] for t in taggings
            if t.get("tag") and t["tag"].get("tag_category")
            and t["tag"]["tag_category"].get("category") == "Mood"
        ])))
        warnings = "|".join(sorted(set([
            t["tag"]["tag"] for t in taggings
            if t.get("tag") and t["tag"].get("tag_category")
            and t["tag"]["tag_category"].get("category") == "Content Warning"
        ])))

        # If default_audio_edition_id exists the book has an audiobook
        # If default_ebook_edition_id exists the book has an ebook
        has_audiobook = result.get("default_audio_edition_id") is not None
        has_ebook     = result.get("default_ebook_edition_id") is not None

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
            "has_audiobook":      has_audiobook,
            "has_ebook":          has_ebook,
            "genres":             genres,
            "moods":              moods,
            "content_warnings":   warnings,
            "description":        result.get("description"),
        }

        fixed_rows.append(row)
        print(f"   Got: {result.get('title')} (rating: {result.get('rating')})")

    else:
        print(f"   Failed for ID: {book['id']}")

    time.sleep(1)

print("\n Patching cosmere_books.csv...")

df = pd.read_csv("data/raw/cosmere_books.csv")

# Define the wrong titles we want to remove
wrong_titles = [
    "Summary Of The Lost Metal: A Mistborn Novel (The Mistborn Saga, 7) By Brandon Sanderson",
    "Brandon Sanderson Sampler: The Way of Kings and Mistborn",
    "Review of Brandon Sanderson's Words of Radiance",
    "Series Order: Brandon Sanderson: Elantris Series: Mistborn Series: Wax and Wayne Series: The Stormlight Archive: Warbreaker Series: Alcatraz Series: Infinity Blade Series: Legion Series",
]

# The ~ symbol means "NOT" — keep everything that is NOT in wrong_titles
df = df[~df["title"].isin(wrong_titles)]

print(f"  Removed wrong rows. Remaining: {len(df)} books")

# Add fixed rows
fixed_df = pd.DataFrame(fixed_rows)
df = pd.concat([df, fixed_df], ignore_index=True)

# Sort by series and series_order so the CSV is neat and logical
series_order = ["Mistborn Era 1", "Mistborn Era 2", "Stormlight Archive", 
                "Elantris", "Warbreaker", "Standalone"]
df["series"] = pd.Categorical(df["series"], categories=series_order, ordered=True)
df = df.sort_values(["series", "series_order"]).reset_index(drop=True)

# Save the patched CSV back
df.to_csv("data/raw/cosmere_books.csv", index=False)

print(f"\n Done! {len(df)} books saved to data/raw/cosmere_books.csv")
print("\n--- Final Preview ---")
print(df[["title", "series", "rating", "ratings_count", "pages"]].to_string())