import numpy as np


def test_preprocessed_shape():
    feature = np.load("data/features/color_0041C3_t4.npy")

    assert len(feature.shape) == 3
    assert feature.shape == (256, 256, 6)


def test_normalized_range():
    feature = np.load(
        "data/normalized_features/color_0041C3_t4.npy"
    )

    assert feature.min() >= -3
    assert feature.max() <= 3
    