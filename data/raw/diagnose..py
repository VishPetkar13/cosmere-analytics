import requests
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/book/show/68428.The_Final_Empire"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, timeout=10)

print("Status code:", response.status_code)
print("\n--- First 3000 characters of HTML ---\n")
print(response.text[:3000])