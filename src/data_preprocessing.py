import pandas as pd
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

def load_data():
    movies_patth = os.path.join(RAW_PATH, "movies.csv")
    ratings_path = os.path.join(RAW_PATH, "ratings.csv")

    movies = pd.read_csv(movies_patth)
    ratings = pd.read_csv(ratings_path)
    return movies, ratings

def preprocess_movies(movies: pd.DataFrame):
    #Remove year from title
    movies['title'] = movies['title'].str.replace(r"\(\d{4}\)", "", regex=True).str.strip()

    #Replacce "|" in genres with space
    movies['genres'] = movies['genres'].str.replace('|', ' ')

    return movies

def merge_data(movies, ratings):
    return pd.merge(ratings, movies, on='moviesId')

def save_processed_data(df: pd.DataFrame, filename="movies_cleaned.csv"):
    df.to_csv(os.path.join(PROCESSED_PATH, filename), index=False)