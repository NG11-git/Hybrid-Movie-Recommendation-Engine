import os
import sys

# Allow importing from src
sys.path.append(os.path.abspath(".."))

from src.data_preprocessing import load_data, preprocess_movies
from src.hybrid import HybridRecommender
from api.services import TMDBServices

class RecommenderService:
    def __init__(self):
        movies, ratings = load_data()
        movies = preprocess_movies(movies)

        self.hybrid = HybridRecommender(movies, ratings)

        # Load trained collaborative model

        self.hybrid.collab_model.load()

        # Load tmdb service
        self.tmdb = TMDBServices()

    def recommend_for_user(self, user_id: int, top_n: int =10):
        
        df = self.hybrid.recommend_for_user(user_id=user_id, top_n=top_n)
        #print("Hybrid output DF:")
        #print(df)
        #print("Is empty:", df.empty)

        enriched = []

        for title in df["title"].tolist():
            movie_data = self.tmdb.search_movie(title)
            #print("TMDB result:", title, movie_data)

            if movie_data:
                enriched.append(movie_data)

        return enriched

    
recommender_services = RecommenderService()

        
