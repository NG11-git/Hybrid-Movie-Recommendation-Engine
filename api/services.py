import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

class TMDBServices:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.cache = {}

    def _clean_title(self, title: str):
        # Remove year from "TOY STORY (1995)"
        return title.rsplit("(", 1)[0].strip()
    
    def search_movie(self, title: str):
        clean_title = self._clean_title(title)

        if clean_title in self.cache:
            return self.cache[clean_title]
        
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": clean_title
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return None
        
        results = response.json().get("results")

        if not results:
            return None
        
        movie = results[0]

        data = {
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster_url": IMAGE_BASE_URL + movie.get("poster_path") if movie.get("poster_path") else None             
        }

        self.cache[clean_title] = data
        return data
