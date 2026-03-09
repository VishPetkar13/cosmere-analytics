SELECT series, ROUND(AVG(rating), 2) average_rating, SUM(ratings_count) total_ratings_count_per_series
FROM books 
GROUP BY series
ORDER BY average_rating DESC