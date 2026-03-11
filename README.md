# 🌌 Cosmere Analytics Engine

> An end-to-end data analytics project exploring Brandon Sanderson's Cosmere universe as a publishing business case.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

## 📖 Project Overview

The Cosmere Analytics Engine treats Brandon Sanderson's interconnected fantasy universe as a real-world publishing dataset. Using data collected from the Hardcover API, this project analyses ratings, reader engagement, book formats, moods, and genres across 19 Cosmere titles to surface insights a publisher would actually care about.

This is a portfolio project built to demonstrate end-to-end data skills — from raw API data collection through to an interactive dashboard.

---

## 🎯 Business Questions This Project Answers

- Which series performs best with readers?
- Do longer books get better ratings?
- Which book should a publisher focus marketing budget on?
- Do darker moods correlate with higher or lower ratings?
- How consistent is quality across a series?
- Which formats (audiobook, ebook) drive more engagement?

---

## 🗂️ Project Structure

```
cosmere-analytics/
│
├── data/
│   ├── raw/                    # Original data from Hardcover API
│   │   ├── collect_data.py     # Main data collection script
│   │   ├── fix_problem_books.py# ID-based correction script
│   │   └── cosmere_books.csv   # Final cleaned dataset (19 books)
│   │
│   └── processed/
│       └── cosmere.db          # SQLite database
│
├── notebooks/
│   └── 01_sql_exploration.ipynb  # SQL queries and initial analysis
│
├── sql/
│   └── explore.sql             # Query library (basic → advanced SQL)
│
├── dashboard/                  # Power BI and Streamlit dashboards (coming soon)
│
├── reports/                    # Final findings and visualisations (coming soon)
│
├── .env                        # API credentials (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

| Field | Details |
|---|---|
| **Source** | [Hardcover.app](https://hardcover.app) GraphQL API |
| **Books** | 19 Cosmere titles |
| **Series** | Mistborn Era 1 & 2, Stormlight Archive, Elantris, Warbreaker, Standalones |
| **Fields** | Title, series, rating, ratings count, pages, release year, genres, moods, content warnings, audiobook/ebook availability |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Collection | Python, Requests, GraphQL |
| Database | SQLite, sqlite3 |
| Analysis | Pandas, Numpy |
| Visualisation | Matplotlib, Seaborn, Power BI |
| Machine Learning | scikit-learn *(coming soon)* |
| Dashboard | Streamlit *(coming soon)* |

---

## 🚀 How To Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/VishPetkar13/cosmere-analytics.git
cd cosmere-analytics
```

### 2. Create and activate virtual environment
```bash
python -m venv vshard
vshard\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Load the database
```bash
python sql/load_database.py
```

### 5. Open the notebook
```bash
jupyter notebook
```
Navigate to `notebooks/01_sql_exploration.ipynb`

---

## 📈 Project Roadmap

- [x] Data collection via Hardcover GraphQL API
- [x] SQLite database setup
- [x] SQL exploration (GROUP BY, Window Functions, CTEs)
- [ ] Python EDA (Matplotlib, Seaborn)
- [ ] Power BI Dashboard
- [ ] Machine Learning — rating prediction model
- [ ] Streamlit Dashboard
- [ ] Portfolio polish and deployment

---

## 👤 Author

**Vishal Petkar**  
MSc Data Analytics graduate interested in data engineering, Python development, machine learning, and building practical data-driven applications.  
[GitHub](https://github.com/VishPetkar13) • [LinkedIn](https://www.linkedin.com/in/vishalpetkar)

---

> *"The most important step a man can take. It's not the first one, is it? It's the next one."* — Brandon Sanderson