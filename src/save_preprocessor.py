"""Save preprocessor pipeline."""

import joblib
import numpy as np

from preprocessor import Preprocessor


x = np.random.rand(10, 5)

preprocessor = Preprocessor()

preprocessor.fit(x)

joblib.dump(
    preprocessor,
    "models/preprocessor.joblib"
)

print("Saved: models/preprocessor.joblib")