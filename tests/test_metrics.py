from src.baseline import always_go_straight
from src.metrics import accuracy, iou, collision_rate


def test_always_go_straight():
    assert always_go_straight() == 0


def test_accuracy():
    assert accuracy([1, 0, 1], [1, 0, 0]) == 2 / 3


def test_iou():
    assert iou(
        [0, 0, 2, 2],
        [1, 1, 3, 3]
    ) == 1 / 7


def test_collision_rate():
    assert collision_rate(2, 10) == 0.2


def test_collision_rate_with_no_trials():
    assert collision_rate(0, 0) == 0
    