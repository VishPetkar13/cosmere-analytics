# ─────────────────────────────────────────────────────────
# COSMERE ANALYTICS — Database Loading Script
#
# This script takes our cleaned CSV and loads it into
# a SQLite database. Think of this as moving our data
# from a flat spreadsheet into a proper queryable database.
#
# Why do this?
# - SQL lets us ask complex questions of our data
# - It mirrors how real companies store and query data
# - Our Jupyter notebooks can query it directly
# ─────────────────────────────────────────────────────────

import sqlite3
import pandas as pd
import os

# ─────────────────────────────────────────────
# STEP 1 — Load our CSV
# ─────────────────────────────────────────────
print("  Loading CSV...")
df = pd.read_csv("data/raw/cosmere_books.csv")
print(f" Loaded {len(df)} books")

# ─────────────────────────────────────────────
# STEP 2 — Clean up data types
# ─────────────────────────────────────────────

df["pages"] = df["pages"].fillna(0).astype(int)

df["release_year"] = df["release_year"].fillna(0).astype(int)

df["rating"] = df["rating"].round(4)

text_columns = ["genres", "moods", "content_warnings", "description"]
for col in text_columns:
    df[col] = df[col].fillna("")

print(" Data types cleaned")

# ─────────────────────────────────────────────
# STEP 3 — Create the SQLite database
# ─────────────────────────────────────────────

os.makedirs("data/processed", exist_ok=True)
db_path = "data/processed/cosmere.db"

print(f"\n Creating Database at {db_path}...")
conn = sqlite3.connect(db_path)

# ─────────────────────────────────────────────
# STEP 4 — Load data into the database
# ─────────────────────────────────────────────

# pandas has a built-in method called to_sql() that
# writes a DataFrame directly into a database table.
#
# if_exists="replace" means: if the table already
# exists, drop it and recreate it. This makes the
# script safe to run multiple times without errors.
#
# index=False means: don't write the DataFrame's
# row numbers (0,1,2...) as a column in the database

df.to_sql("books", conn, if_exists="replace", index=False)
print("   Table 'books' created and loaded ")

# ─────────────────────────────────────────────
# STEP 5 — Verify it worked
# ─────────────────────────────────────────────

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM books")
count = cursor.fetchone()[0]
print(f"\n Database loaded successfully")
print(f" Total books in database: {count}")

# preview the table structure
print (f"\n --- Column Names ---")
cursor.execute("PRAGMA table_info(books)")
columns = cursor.fetchall()
for col in columns:
    print(f" {col[1]:25} {col[2]}")

print(f"\n --- Sample Data ---")
cursor.execute("""
    SELECT title, series, rating, ratings_count, pages
    FROM books
    ORDER BY series, series_order
    LIMIT 5
""")
rows = cursor.fetchall()
for row in rows:
    print(f"   {row}")

conn.close()
print(f"\n Connection closed.")
print(f"   Database saved at: {db_path}")