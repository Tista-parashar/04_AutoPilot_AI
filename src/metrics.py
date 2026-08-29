"""Functions for evaluating model performance."""


def accuracy(predictions, labels):
    """Calculate the accuracy of predictions.

    Args:
        predictions: The predicted labels.
        labels: The actual labels.

    Returns:
        The proportion of correct predictions.
    """
    correct = 0

    for prediction, label in zip(predictions, labels):
        if prediction == label:
            correct += 1

    return correct / len(labels)


def iou(predicted_box, actual_box):
    """Calculate Intersection over Union for two bounding boxes.

    Args:
        predicted_box: Coordinates of the predicted box.
        actual_box: Coordinates of the actual box.

    Returns:
        The IoU value between 0 and 1.
    """
    x1 = max(predicted_box[0], actual_box[0])
    y1 = max(predicted_box[1], actual_box[1])
    x2 = min(predicted_box[2], actual_box[2])
    y2 = min(predicted_box[3], actual_box[3])

    intersection_width = max(0, x2 - x1)
    intersection_height = max(0, y2 - y1)

    intersection = intersection_width * intersection_height

    predicted_area = (
        predicted_box[2] - predicted_box[0]
    ) * (
        predicted_box[3] - predicted_box[1]
    )

    actual_area = (
        actual_box[2] - actual_box[0]
    ) * (
        actual_box[3] - actual_box[1]
    )

    union = predicted_area + actual_area - intersection

    if union == 0:
        return 0

    return intersection / union


def collision_rate(collisions, total_trials):
    """Calculate the rate of collisions.

    Args:
        collisions: Number of collisions.
        total_trials: Total number of trials.

    Returns:
        The proportion of trials that resulted in collisions.
    """
    if total_trials == 0:
        return 0

    return collisions / total_trials
