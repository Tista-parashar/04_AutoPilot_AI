import os
import json


def test_train_split_exists():
    """Check that the training split file exists."""
    assert os.path.exists("train_split.json")


def test_val_split_exists():
    """Check that the validation split file exists."""
    assert os.path.exists("val_split.json")


def test_test_split_exists():
    """Check that the test split file exists."""
    assert os.path.exists("test_split.json")


def test_split_files_are_valid():
    """Check that all split files contain valid JSON lists."""
    files = ["train_split.json", "val_split.json", "test_split.json"]

    for file_name in files:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, list)
        assert len(data) > 0
