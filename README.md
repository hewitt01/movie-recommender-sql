# movie-recommender-sql
A command-line tool that helps you discover movies using real rating data from the MovieLens dataset. It offers two ways to explore:

Hidden Gems — well-rated movies that haven't been widely seen, found by filtering for a moderate number of ratings and sorting by average score.
Fan Favorites — recommendations based on your favorite movie, found by looking at what other people who also loved that movie rated highly. This is a simplified version of the collaborative filtering approach used by services like Netflix and Spotify.


Tech Stack

Python — pandas for data handling, sqlite3 for database access
SQL — joins, aggregation (GROUP BY, HAVING), subqueries, parameterized queries
SQLite — lightweight local database, built from the MovieLens CSV files
Matplotlib — visualizing rating trends by genre


How It Works

load_data.py loads the MovieLens CSV files into a local SQLite database (movies.db).
analysis.py runs a small command-line menu that lets you choose between the two features above.
When you search for a movie, the tool does a fuzzy title search first (so you don't need to type the exact title/year) and asks you to confirm if there are multiple matches.
Recommendations are generated using a nested SQL query: first finding everyone who rated your chosen movie highly, then finding what else that group of people rated highly — excluding the original movie itself.


Setup

Download the "ml-latest-small" dataset and place movies.csv and ratings.csv in this project folder.
Install dependencies:
   pip install pandas matplotlib
Build the local database (only needs to be run once):
   python load_data.py
Run the tool:
   python analysis.py
Example Usage
What would you like to do?
1. Find hidden gems
2. Get recommendations based on a favorite movie
Enter 1 or 2: 2
What's your favorite movie? toy story
Did you mean one of these?
1. Toy Story (1995)
2. Toy Story 2 (1999)
3. Toy Story 3 (2010)
Enter the number: 2

Fans of Toy Story 2 (1999) also loved (based on shared fans):
                                        title  avg_rating  shared_fans
0  Star Wars: Episode IV - A New Hope (1977)    4.71           26
1                            Toy Story (1995)    4.61           27
2                                Shrek (2001)    4.52           23
...
What I Learned / Key Design Decisions
Relational data design and joins. The MovieLens data is split across two tables (movies and ratings) that only share a movieId key — no titles live in the ratings table at all. Working with this structure meant thinking in terms of relationships between tables rather than a single flat spreadsheet, and using JOIN to reconstruct a complete picture (which movie each rating actually belongs to) before any analysis could happen.

Small sample sizes distort averages. Movies with very few ratings are far more likely to show extreme (very high or very low) averages purely by chance, compared to movies with hundreds of ratings. This is why every query in the project enforces a minimum ratings threshold — without it, "top rated" results would mostly reflect statistical noise rather than genuine quality.

User input should never be trusted directly in a query. Any value coming from user input (like a searched movie title) is passed through parameterized queries (? placeholders) rather than inserted directly into the SQL string. This protects against SQL injection and is standard practice even in small, single-user tools like this one

Dataset

This project uses the MovieLens "small" dataset (~100,000 ratings) from GroupLens Research, University of Minnesota.
