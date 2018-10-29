from operator import itemgetter

from utils.region_tracker import RegionTracker


def initialise_region_tracker(id, entries, exits):
    movements1 = [(t, r, True) for t, r in entries] + [(t, r, False) for t, r in exits]
    movements1.sort(key=itemgetter(0))
    return RegionTracker(0, movements1)


def test_average_stay_time_basic():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time() == 2.5


def test_average_stay_time_missing_entry():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(2, 'c'), (4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time() == 2.5


def test_average_stay_time_lower_bound():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time(start_time=3) == 2


def test_average_stay_time_upper_bound():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time(end_time=7) == 3


def test_average_stay_time_sandwiched():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time(start_time=3, end_time=9) == 2


def test_average_stay_time_sandwiched_divison_by_zero():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.average_stay_time(start_time=1, end_time=2) == 0


def test_bounce_rate_basic():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.bounce_rate(2) == 0.5


def test_bounce_rate_missing_entry():
    entries1 = [(1, 'a'), (6, 'b')]
    exits1 = [(3, 'c'), (4, 'a'), (8, 'b')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.bounce_rate(2) == 0.5


def test_bounce_rate_empty():
    entries1 = []
    exits1 = []
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.bounce_rate(2) == 0


def test_bounce_rate_advanced():
    entries1 = [(1, 'a'), (6, 'b'), (10, 'c'), (11, 'b'), (90, 'a')]
    exits1 = [(4, 'a'), (8, 'b'), (19, 'c'), (12, 'b'), (91, 'a')]
    region1 = initialise_region_tracker(1, entries1, exits1)
    assert region1.bounce_rate(2) == 0.6