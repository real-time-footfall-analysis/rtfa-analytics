from analytics.state import Person


def test_basic_get_location():
    entries1 = [(1, 'a')]
    exits1 = [(3, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(2) == 'a'


def test_get_location_with_person_exiting():
    entries1 = [(1, 'a')]
    exits1 = [(3, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(5) is None


def test_get_location_with_2_entries_2_exits_1():
    entries1 = [(1, 'a'), (3, 'b')]
    exits1 = [(5, 'a'), (7, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(4) == 'b'


def test_get_location_with_2_entries_2_exits_2():
    entries1 = [(1, 'a'), (3, 'b')]
    exits1 = [(5, 'a'), (7, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(6) == 'b'


def test_get_location_with_3_entries_3_exits_3():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(3, 'k'), (8, 'a'), (10, 'b')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(2) == 'k'


def test_get_location_with_3_entries_3_exits_4():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(3, 'k'), (8, 'b'), (10, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(9) == 'a'


def test_get_location_with_3_entries_3_exits_5():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'b'), (10, 'a'), (12, 'k')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(11) == 'k'


def test_get_location_with_3_entries_3_exits_6():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'k'), (10, 'b'), (12, 'a')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(11) == 'a'


def test_get_location_with_no_exits():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(11) == 'b'


def test_get_location_with_no_entries():
    exits1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    entries1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(11) is None


def test_get_location_with_t_before_first_entry():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = [(8, 'b'), (10, 'a'), (12, 'k')]
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(0) is None


def test_get_location_with_t_after_last_entry():
    entries1 = [(1, 'k'), (4, 'a'), (6, 'b')]
    exits1 = []
    movements1 = [(t, r, True) for t, r in entries1] + [(t, r, False) for t, r in exits1]
    p1 = Person(movements1)
    assert p1.get_location(382) == 'b'