import os
import pandas as pd
from surprise import SVD
from surprise import Dataset, Reader
from surprise import accuracy
from surprise.model_selection import cross_validate, train_test_split
import joblib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models")

class CollaborativeRecommender:
    def __init__(self):
        self.model = SVD()

    def train(self, ratings: pd.DataFrame):
        reader = Reader(rating_scale=(0.5, 5.0))

        data  = Dataset.load_from_df(
            ratings[['userId', 'movieId', 'rating']], reader
        )

        trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

        self.model.fit(trainset)

        predictions = self.model.test(testset)
        print("RMSE:", accuracy.rmse(predictions))

        joblib.dump(self.model, os.path.join(MODEL_PATH, "svd_model.pkl"))

    def load(self):
        self.model = joblib.load(os.path.join(MODEL_PATH, "svd_model.pkl"))

    def predict_rating(self, user_id, movies_id):
        return self.model.predict(user_id, movies_id).est