import pandas as pd
import sqlite3

conn = sqlite3.connect('data/processed/cosmere.db')
df = pd.read_sql_query('SELECT * FROM books', conn)
conn.close()

df['moods'] = df['moods'].str.split('|')
moods_df = df[['title', 'series', 'moods']].explode('moods')
moods_df['moods'] = moods_df['moods'].str.strip('"[] ').str.lower()
moods_df = moods_df[moods_df['moods'].str.strip() != '']
moods_df = moods_df[~moods_df['moods'].str.isdigit()]
moods_df = moods_df[moods_df['moods'].str.len() > 2]

moods_df.to_csv('data/processed/cosmere_moods.csv', index=False)
print(f'Done! {len(moods_df)} mood rows exported')