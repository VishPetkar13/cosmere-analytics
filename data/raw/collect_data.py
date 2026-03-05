import request
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

books = [
    # --- Mistborn Era 1 ---
    {"title": "The Final Empire",         "series": "Mistborn Era 1", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/68428.The_Final_Empire"},
    {"title": "The Well of Ascension",    "series": "Mistborn Era 1", "series_order": 2, "goodreads_url": "https://www.goodreads.com/book/show/68429.The_Well_of_Ascension"},
    {"title": "The Hero of Ages",         "series": "Mistborn Era 1", "series_order": 3, "goodreads_url": "https://www.goodreads.com/book/show/2767793.The_Hero_of_Ages"},

    # --- Mistborn Era 2 ---
    {"title": "The Alloy of Law",         "series": "Mistborn Era 2", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/10803121-the-alloy-of-law"},
    {"title": "Shadows of Self",          "series": "Mistborn Era 2", "series_order": 2, "goodreads_url": "https://www.goodreads.com/book/show/16065004-shadows-of-self"},
    {"title": "The Bands of Mourning",    "series": "Mistborn Era 2", "series_order": 3, "goodreads_url": "https://www.goodreads.com/book/show/18739426-the-bands-of-mourning"},

    # --- Stormlight Archive ---
    {"title": "The Way of Kings",         "series": "Stormlight Archive", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/7235533-the-way-of-kings"},
    {"title": "Words of Radiance",        "series": "Stormlight Archive", "series_order": 2, "goodreads_url": "https://www.goodreads.com/book/show/17332218-words-of-radiance"},
    {"title": "Oathbringer",              "series": "Stormlight Archive", "series_order": 3, "goodreads_url": "https://www.goodreads.com/book/show/34002132-oathbringer"},
    {"title": "Rhythm of War",            "series": "Stormlight Archive", "series_order": 4, "goodreads_url": "https://www.goodreads.com/book/show/49021976-rhythm-of-war"},
    {"title": "Wind and Truth",           "series": "Stormlight Archive", "series_order": 5, "goodreads_url": "https://www.goodreads.com/book/show/57975287-wind-and-truth"},

    # --- Elantris ---
    {"title": "Elantris",                 "series": "Elantris", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/68427.Elantris"},

    # --- Warbreaker ---
    {"title": "Warbreaker",               "series": "Warbreaker", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/1268479.Warbreaker"},

    # --- Standalone / Other ---
    {"title": "The Rithmatist",           "series": "Standalone", "series_order": 1, "goodreads_url": "https://www.goodreads.com/book/show/14497.The_Rithmatist"},
    {"title": "Tress of the Emerald Sea", "series": "Standalone", "series_order": 2, "goodreads_url": "https://www.goodreads.com/book/show/60531406-tress-of-the-emerald-sea"},
]

def scrape_goodreads(url):

    headers = {"User_Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        script_tag = soup.find("script", {"type": "application/ld+json"})

        if script_tag:
            data = json.loads(script_tag.string)

            rating       = data.get("aggregateRating", {}).get("ratingValue", None)
            rating_count = data.get("aggregateRating", {}).get("ratingCount", None)
            review_count = data.get("aggregateRating", {}).get("reviewCount", None)
            page_count   = data.get("numberOfPages", None)
            description  = data.get("description", None)
            pub_date     = data.get("datePublished", None)

            return {
                "goodreads_rating":        float(rating) if rating else None,
                "goodreads_ratings_count": int(rating_count) if rating_count else None,
                "goodreads_reviews_count": int(review_count) if review_count else None,
                "page_count":              int(page_count) if page_count else None,
                "description":             description,
                "publication_year":        int(pub_date[:4]) if pub_date else None,
            }
        
    except Exception as e:
        print(f" Error Scraping {url}: {e}")

    return {
        "goodreads_rating": None,
        "goodreads_ratings_count": None,
        "goodreads_reviews_count": None,
        "page_count": None,
        "description": None,
        "publication_year": None,
    }    

all_books = []

for book in books:
    print(f" Scraping: {book['title']}...")
    scraped_data = scrape_goodreads(book["goodreads_url"])

    combined = {**book, **scraped_data}

    all_books.append(combined)

    time.sleep(2)


df = pd.DataFrame(all_books)

df = df.drop(columns=['goodreads_url'])

df.to_csv("data/raw/cosmere_books.csv", index=False)

print("\n Done! Data saved to data/raw/cosmere_books.csv")
print(df)