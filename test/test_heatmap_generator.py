from operator import itemgetter

from utils.heatmap_generator import HeatmapGenerator
from utils.region_tracker import RegionTracker


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


def test_build_heatmap_basic():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    m1 = initialise_user_movements(1, entries1, exits1)

    entries2 = [(1, 'b')]
    exits2 = [(9, 'b')]
    m2 = initialise_user_movements(2, entries2, exits2)

    heatmap_gen = HeatmapGenerator(1, merge_user_movements(m1, m2))

    expected_at_2 = {'a':1, 'b': 1}
    expected_at_10 = {}
    assert expected_at_2 == heatmap_gen.build_heat_map(2)
    assert expected_at_10 == heatmap_gen.build_heat_map(10)


def test_build_heatmap_advanced():
    entries1 = [(2, 'a'), (4, 'b')]
    exits1 = [(6, 'a'), (8, 'b')]
    m1 = initialise_user_movements(1, entries1, exits1)

    entries2 = [(1, 'b')]
    exits2 = [(19, 'b')]
    m2 = initialise_user_movements(2, entries2, exits2)

    entries3 = [(1, 'a'), (3, 'a')]
    exits3 = [(2, 'a'), (7, 'a')]
    m3 = initialise_user_movements(3, entries3, exits3)

    heatmap_gen = HeatmapGenerator(1, merge_user_movements(m1, m2, m3))

    expected_at_5 = {'a':1, 'b': 2}
    expected_at_19 = {}
    assert expected_at_5 == heatmap_gen.build_heat_map(5)
    assert expected_at_19 == heatmap_gen.build_heat_map(19)


def test_build_heatmap_no_exit():
    entries1 = [(2, 'a'), (4, 'b')]
    exits1 = [(6, 'a')]
    m1 = initialise_user_movements(1, entries1, exits1)
    heatmap_gen = HeatmapGenerator(1, m1)

    assert heatmap_gen.build_heat_map(100) == {'b':1}


def test_build_heatmap_history_basic_auto_duration():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    m1 = initialise_user_movements(1, entries1, exits1)

    entries2 = [(1, 'b')]
    exits2 = [(9, 'b')]
    m2 = initialise_user_movements(2, entries2, exits2)

    heatmap_gen = HeatmapGenerator(1, merge_user_movements(m1, m2))

    expected_at_3 = {'a':1, 'b': 1}
    expected_at_5 = {'b':1}
    expected_at_7 = {'b':2}
    expected_at_9 = {}
    expected_at_11 = {}

    expected = {'3':expected_at_3, '5':expected_at_5, '7':expected_at_7, '9':expected_at_9, '11':expected_at_11}
    assert expected == heatmap_gen.build_heat_map_history(2)[1]


def test_heatmap_history_with_appended_movements_halfway_1():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a')]
    m1 = initialise_user_movements(1, entries1, exits1)

    entries2 = [(1, 'b')]
    exits2 = []
    m2 = initialise_user_movements(2, entries2, exits2)

    heatmap_gen = HeatmapGenerator(1, merge_user_movements(m1, m2))

    expected_at_3 = {'a':1, 'b': 1}
    expected_at_5 = {'b':1}
    expected_at_7 = {'b':2}

    expected = {'3':expected_at_3, '5':expected_at_5, '7': expected_at_7}
    assert expected == heatmap_gen.build_heat_map_history(2)[1]

    entries1 = [(10, 'c')]
    exits1 = [(12, 'c'), (13, 'c')]
    m1 = initialise_user_movements(1, entries1, exits1)

    start_time = heatmap_gen.last_movement
    heatmap_gen.append_movements(m1)

    expected_at_8 = {'b':2}
    expected_at_10 = {'b': 2}
    expected_at_12 = {'b':2}
    expected_at_14 = {'b':2}

    expected = {'3':expected_at_3, '5':expected_at_5, '7':expected_at_7, '8':expected_at_8, '10':expected_at_10,
                '12':expected_at_12, '14': expected_at_14}
    assert expected == heatmap_gen.build_heat_map_history(2)[1]
