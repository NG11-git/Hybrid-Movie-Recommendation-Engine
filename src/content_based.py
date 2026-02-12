import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models")

class ContentBasedRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.similarity_matrix = None
        self.movies = None

    def train(self, movies: pd.DataFrame):
        self.movies = movies.reset_index(drop=True)

        tfidf_matrix = self.vectorizer.fit_transform(self.movies['genres'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix)

        joblib.dump(self.vectorizer, os.path.join(MODEL_PATH, "tfidf_vectorizer.pkl"))
        joblib.dump(self.similarity_matrix, os.path.join(MODEL_PATH, "content_similarity.pkl"))

    def get_similar_movies(self, movie_title, top_n=10):
        idx = self.movies[self.movies['title'] == movie_title].index[0]

        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        movie_indices = [i[0] for i in scores[1: top_n + 1]]

        return self.movies.iloc[movie_indices][["title", "genres"]]