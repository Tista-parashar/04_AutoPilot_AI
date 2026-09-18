import pandas as pd
import json
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/iris.csv")

print(df.head())

train, temp = train_test_split(
    df,
    test_size=0.30,
    stratify=df["species"],
    random_state=42
)

print(len(train))
print(len(temp))

val, test = train_test_split(
    temp,
    test_size=0.50,
    stratify=temp["species"],
    random_state=42
)

print(len(val))
print(len(test))

with open("train_split.json", "w", encoding="utf-8") as file:
    json.dump(train.index.tolist(), file)

    with open("val_split.json", "w", encoding="utf-8") as file:
        json.dump(val.index.tolist(), file)

with open("test_split.json", "w", encoding="utf-8") as file:
    json.dump(test.index.tolist(), file)

    print("Train class balance:")
print(train["species"].value_counts())

print("Validation class balance:")
print(val["species"].value_counts())

print("Test class balance:")
print(test["species"].value_counts())
