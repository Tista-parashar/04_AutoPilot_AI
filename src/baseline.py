"""Simple baseline strategy for the autopilot project."""


def always_go_straight():
    """Return the action representing going straight.

    Returns:
        An integer representing the straight-ahead action.
    """
    return 0


if __name__ == "__main__":
    ACTION= always_go_straight()
    print("Baseline action:", ACTION)
