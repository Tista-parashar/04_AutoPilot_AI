import os
import json
import joblib
import numpy as np

from sklearn.preprocessing import StandardScaler


# -------------------------
# IMAGE NORMALIZATION
# -------------------------

with open("data/mean_std.json", "r") as f:
    stats = json.load(f)

mean = np.array(stats["mean"])
std = np.array(stats["std"])

print("Mean:", mean)
print("Std:", std)

# Save normalization parameters
norm_params = {
    "mean": stats["mean"],
    "std": stats["std"]
}

with open("data/norm_params.json", "w") as f:
    json.dump(norm_params, f, indent=4)

print("Saved: data/norm_params.json")


# -------------------------
# FEATURE STANDARDIZATION
# -------------------------

feature_dir = "data/features"

feature_vectors = []
feature_files = []

for file in os.listdir(feature_dir):
    if file.endswith(".npy"):
        path = os.path.join(feature_dir, file)

        feature = np.load(path)

        feature_vectors.append(feature.flatten())
        feature_files.append(file)

feature_vectors = np.array(feature_vectors)

print("Feature matrix shape:", feature_vectors.shape)

scaler = StandardScaler()

scaled_features = scaler.fit_transform(feature_vectors)

joblib.dump(scaler, "data/feature_scaler.pkl")

print("Saved: data/feature_scaler.pkl")


# -------------------------
# SAVE NORMALIZED FEATURES
# -------------------------

output_dir = "data/normalized_features"
os.makedirs(output_dir, exist_ok=True)

for file, feature in zip(feature_files, scaled_features):
    save_path = os.path.join(output_dir, file)
    np.save(save_path, feature)

print(f"Saved {len(feature_files)} normalized feature files")
