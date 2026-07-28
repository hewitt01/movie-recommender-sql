import pandas as pd
import sqlite3

connection = sqlite3.connect("movies.db")

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

movies.to_sql("movies", connection, if_exists="replace", index=False) #what is index and why do we assign it to false here
ratings.to_sql("ratings", connection, if_exists="replace", index=False)

connection.close()
print("Data loaded successfully!!")
print(movies.head())
print(ratings.head())