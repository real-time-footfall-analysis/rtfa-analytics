from analytics.state import Person, EventState


def test_basic_get_location():
    entries1 = [(1, 'a')]
    exits1 = [(3, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(2) == 'a'


def test_get_location_with_person_exiting():
    entries1 = [(1, 'a')]
    exits1 = [(3, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(5) is None


def test_get_location_with_2_entries():
    entries1 = [(1, 'a'), (5, 'a')]
    exits1 = [(3, 'a'), (10, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(0) is None
    assert p1.get_location(2) == 'a'
    assert p1.get_location(4) is None
    assert p1.get_location(7) == 'a'


def test_get_location_with_2_entries_2_exits_1():
    entries1 = [(1, 'a'), (3, 'b')]
    exits1 = [(5, 'a'), (7, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(4) == 'b'


def test_get_location_with_2_entries_2_exits_2():
    entries1 = [(1, 'a'), (3, 'b')]
    exits1 = [(5, 'a'), (7, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(6) == 'b'


def test_get_location_with_3_entries_3_exits_3():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(3, 'k'), (8, 'a'), (10, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(2) == 'k'


def test_get_location_with_3_entries_3_exits_4():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(3, 'k'), (8, 'b'), (10, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(9) == 'a'


def test_get_location_with_3_entries_3_exits_5():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'b'), (10, 'a'), (12, 'k')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(11) == 'k'


def test_get_location_with_3_entries_3_exits_6():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'k'), (10, 'b'), (12, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(11) == 'a'


def test_get_location_with_no_exits():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(11) == 'b'


def test_get_location_with_no_entries():
    exits1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    entries1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(11) is None


def test_get_location_with_t_before_first_entry():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'b'), (10, 'a'), (12, 'k')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(0) is None


def test_get_location_with_t_after_last_entry():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_location(382) == 'b'


def test_empty_get_next_location():
    entries1 = []
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(2) is None


def test_basic_get_next_location_1():
    entries1 = [(3, 'a')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(2) is None


def test_basic_get_next_location_2():
    entries1 = [(3, 'a')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(4) == 'a'


def test_iteration_get_next_location_1():
    entries1 = [(3, 'a'), (6, 'b')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(4) == 'a'
    assert p1.get_next_location(4) == 'b'


def test_iteration_get_next_location_with_exits_1():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(1) is None
    assert p1.get_next_location(2) == 'a'
    assert p1.get_next_location(2) is None
    assert p1.get_next_location(2) == 'b'
    assert  p1.get_next_location(2) is None
    assert p1.get_next_location(2) is None


def test_iteration_with_reset():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)
    assert p1.get_next_location(2) == 'a'
    assert p1.get_next_location(2) is None
    p1.reset_iteration()
    assert p1.get_next_location(2) == 'a'


def test_build_heatmap_basic():
    entries1 = [(2, 'a'), (6, 'b')]
    exits1 = [(4, 'a'), (8, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)

    entries2 = [(1, 'b')]
    exits2 = [(9, 'b')]
    movements2 = [(t, r, True) for t, r in entries2] + [(t, r, False) for t, r in exits2]
    p2 = Person(1, movements2)

    event = EventState()
    event.people = {p1.id: p1, p2.id: p2}

    expected_at_2 = {'a':1, 'b': 1}
    expected_at_10 = {}
    assert expected_at_2 == event.build_heat_map(2)
    assert expected_at_10 == event.build_heat_map(10)


def test_build_heatmap_advanced():
    entries1 = [(2, 'a'), (4, 'b')]
    exits1 = [(6, 'a'), (8, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(0, movements1)

    entries2 = [(1, 'b')]
    exits2 = [(19, 'b')]
    movements2 = [(t, r, True) for t, r in entries2] + [(t, r, False) for t, r in exits2]
    p2 = Person(1, movements2)

    entries3 = [(1, 'a'), (3, 'a')]
    exits3 = [(2, 'a'), (7, 'a')]
    movements3 = [(t, r, True) for t, r in entries3] + [(t, r, False) for t, r in exits3]
    p3 = Person(2, movements3)

    event = EventState()
    event.people = {p1.id: p1, p2.id: p2, p3.id: p3}

    expected_at_5 = {'a':1, 'b': 2}
    expected_at_19 = {}
    assert expected_at_5 == event.build_heat_map(5)
    assert expected_at_19 == event.build_heat_map(19)

