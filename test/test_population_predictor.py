from operator import itemgetter


def initialise_user_movements(id, entries, exits):
    movements = [(id, t, r, True) for t, r in entries] + [(id, t, r, False) for t, r in exits]
    movements.sort(key=itemgetter(1))
    return movements


def merge_user_movements(*users):
    all_movements = []
    for user in users:
        all_movements += user
    all_movements.sort(key=itemgetter(1))
    return all_movements


def test_build_prediction_basic():
    pass