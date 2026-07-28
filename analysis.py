import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

connection = sqlite3.connect("movies.db")

def get_hidden_gems(connection, min_ratings = 20, max_ratings = 100, limit = 15):
    query = """
    SELECT movies.title, AVG(ratings.rating) as avg_rating, COUNT(*) as total_ratings
    FROM ratings
    JOIN movies ON ratings.movieId = movies.movieId
    GROUP BY movies.title
    HAVING COUNT(*) BETWEEN ? AND ?
    ORDER BY avg_rating DESC
    LIMIT ?
    """
    try:
        return pd.read_sql_query(query, connection, params=(min_ratings, max_ratings, limit))
    except Exception as e:
        print(e)
        return pd.DataFrame()

def recommended_movies(connection, movie_title, min_rating=4.5, min_shared_fans=20, limit=10):
    query = """
    SELECT movies.title, AVG(ratings.rating) as avg_rating, COUNT(*) as shared_fans
    FROM ratings
    JOIN movies ON ratings.movieId = movies.movieId
    WHERE ratings.userId IN (
        SELECT userId FROM ratings 
        WHERE movieId = (SELECT movieId FROM movies WHERE title = ?)
        AND rating >= ?
    )
    AND movies.title != ?
    GROUP BY movies.title
    HAVING COUNT(*) >= ?
    ORDER BY avg_rating DESC
    LIMIT ?
    """
    try:
        return pd.read_sql_query(
            query, connection, 
            params=(movie_title, min_rating, movie_title, min_shared_fans, limit)
        )
    except Exception as e:
        print(e)
        return pd.DataFrame()

def find_movie_title(connection, search_term):
    query = "SELECT title FROM movies WHERE title LIKE ? LIMIT 5"
    try:
        results = pd.read_sql_query(query, connection, params=(f"%{search_term}%",))
        return results
    except Exception as e:
        print(e)
        return pd.DataFrame()


def main():
    connection = sqlite3.connect("movies.db")
    try:
        print("What would you like to do?")
        print("1. Find hidden gems")
        print("2. Get recommendations based on a favorite movie")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            hidden_gems = get_hidden_gems(connection)
            print("                                === Hidden Gems ===")
            print(hidden_gems)
        elif choice == "2":
            favorite = input("What's your favorite movie? ")
            matches = find_movie_title(connection, favorite)

            if matches.empty:
                print(f"Sorry, couldn't find any movie matching '{favorite}'.")
                return

            # If multiple matches found
            if len(matches) > 1:
                print("\nDid you mean one of these?")
                for i, title in enumerate(matches["title"]):
                    print(f"{i + 1}. {title}")
                choice = int(input("Enter the number: ")) - 1
                exact_title = matches["title"].iloc[choice]
            else:
                exact_title = matches["title"].iloc[0]

            similar = recommended_movies(connection, exact_title)

            if similar.empty:
                print(f"No strong recommendations found for '{exact_title}' (maybe too few ratings).")
            else:
                print(f"\nSince you liked {exact_title}, you might also enjoy:")
                print(similar)
        else:
            print("invalid option chosen")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
