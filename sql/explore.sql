-- Average rating and total ratings per series
-- sorted by highest rated
SELECT series, ROUND(AVG(rating), 2) average_rating, SUM(ratings_count) total_ratings_count_per_series
FROM books 
GROUP BY series
ORDER BY average_rating DESC


--Books which are the best and worst performers in each series
SELECT title, series, rating, ROW_NUMBER() OVER (PARTITION BY series ORDER BY rating DESC) as ranking_by_series
FROM books

-- best performing book in each series
WITH best_performer AS (
SELECT title, series, rating, ROW_NUMBER() OVER (PARTITION BY series ORDER BY rating DESC) as ranking_by_series
FROM books)
SELECT title, series, rating
FROM best_performer
WHERE ranking_by_series = 1