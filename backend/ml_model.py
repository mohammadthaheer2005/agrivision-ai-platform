import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

class YieldPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model_path = os.path.join(os.path.dirname(__file__), "yield_model.pkl")
        self._initialize_dummy_model()

    def _initialize_dummy_model(self):
        """
        Train a quick dummy model if no model exists so the API works immediately.
        Features: [Rainfall, Temperature, Fertilizer, Pesticide]
        """
        if not os.path.exists(self.model_path):
            # Generating synthetic data
            np.random.seed(42)
            X = np.random.rand(100, 4) * 100 # Random stats
            y = 2*X[:,0] + 0.5*X[:,1] + 1.2*X[:,2] - 0.3*X[:,3] + np.random.normal(0, 5, 100)
            
            self.model.fit(X, y)
            joblib.dump(self.model, self.model_path)
        else:
            self.model = joblib.load(self.model_path)

    def predict(self, rainfall, temp, fertilizer, pesticide):
        features = np.array([[rainfall, temp, fertilizer, pesticide]])
        prediction = self.model.predict(features)
        return float(prediction[0])

# Global instance
predictor = YieldPredictor()
