import sys
import os

sys.path.append(os.path.abspath(".."))


import pandas as pd
from src.content_based import ContentBasedRecommender
from src.collaborative import CollaborativeRecommender

class HybridRecommender:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

        self.content_model = ContentBasedRecommender()
        self.collab_model = CollaborativeRecommender()

    def recommend_for_user(self, user_id, top_n=10):
        movies_ids = self.movies["movieId"].unique()

        scores = []

        for movie_id in movies_ids:
            collab_score = self.collab_model.predict_rating(user_id, movie_id)
            
            # For hybrid simplicity normalize content score by average genres similarity
            movie_title = self.movies[self.movies["movieId"] == movie_id]["title"].values[0]

            try:
                content_similar = self.content_model.get_similar_movies(movie_title, top_n=5)
                conten_score =0.5
            except:
                content_score = 0

            final_scores = 0.7 * collab_score + 0.3 * content_score

            scores.append((movie_id, final_scores))

        scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]

        recommended_ids = [i[0] for i in scores]

        return self.movies[self.movies["movieId"].isin(recommended_ids)]