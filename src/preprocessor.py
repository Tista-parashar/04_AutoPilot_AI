"""Reusable preprocessing pipeline."""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class Preprocessor:
    """End-to-end preprocessing pipeline."""

    def __init__(self):
        self.pipeline = Pipeline([
            ("scaler", StandardScaler())
        ])

    def fit(self, x, y=None):
        """Fit preprocessing pipeline."""
        self.pipeline.fit(x)
        return self

    def transform(self, x):
        """Transform input data."""
        return self.pipeline.transform(x)
