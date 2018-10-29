import bisect
from collections import OrderedDict
from operator import itemgetter

from collections import defaultdict


class EventState:

    # Maintains list of people at an event, and can efficiently build position maps.

    def __init__(self, event, people=None):

        # Meta data.
        self.event = event
        self.first_movement = None
        self.last_movement = None

        # Maps person_id -> person object.
        self.people = {} if people is None else people

    def build_heat_map(self, t):
        # Builds a heat-map by region at a particular timestamp t. DO NOT use this function iteratively,
        # for an efficient iterative version use build_heat_map_history.
        regions = defaultdict(int)
        for person in self.people.values():
            location = person.get_location(t)
            if location is not None:
                regions[person.get_location(t)] += 1
        return regions

    def build_heat_map_history(self, time_interval, duration=None):
        # Efficiently iterates through people, adding their location data to a history of heatmaps at a given
        # time_interval.
        heatmaps = defaultdict(lambda: defaultdict(int))
        duration = duration if duration is not None else self.last_movement
        for person in self.people.values():
            time = self.first_movement
            time_end = self.first_movement + duration
            while time + time_interval <= time_end:
                time += time_interval
                location = person.get_next_location(time_interval)
                if location is not None:
                    heatmaps[time][location] += 1
        return heatmaps


class Person:

    # Maintains state of a single persons location throughout event.
    # Movements are of type [(timestamp, region, entered)], and are SORTED.
    # Entered is a boolean specifying if the region has been entered or exited.

    def __init__(self, uid, movements=None):

        # Meta data.
        self.id = uid

        # Movement storage.
        self.entries, self.exits = [], []
        if movements is not None:
            assert all([movements[i-1][0] <= movements[i][0] for i in range(1, len(movements))])
            for (timestamp, region, entered) in movements:
                if entered:
                    self.entries.append((timestamp, region))
                else:
                    self.exits.append((timestamp, region))

        # Used for iteration over events.
        self.entry_event_pointer = 0
        self.exit_event_pointer = 0
        self.time_pointer = 0
        self.current_locations = OrderedDict()

    def reset_iteration(self):
        self.entry_event_pointer = 0
        self.exit_event_pointer = 0
        self.time_pointer = 0
        self.current_locations = OrderedDict()

    def has_more_movements(self):
        # Returns whether there are more movements to receive from iterator.
        return self.entry_event_pointer < len(self.entries) or self.exit_event_pointer < len(self.exits)

    def get_next_location(self, time_interval):

        # Increase time pointer by set interval.
        self.time_pointer += time_interval

        # Add entries to ordered dict and remove exits from ordered dict sequentially (important).
        while (self.entry_event_pointer < len(self.entries) and
                       self.entries[self.entry_event_pointer][0] <= self.time_pointer) or \
                (self.exit_event_pointer < len(self.exits) and
                        self.exits[self.exit_event_pointer][0] <= self.time_pointer):
            next_entry_time = self.entries[self.entry_event_pointer][0] if self.entry_event_pointer < len(self.entries) else float('inf')
            next_exit_time = self.exits[self.exit_event_pointer][0] if self.exit_event_pointer < len(self.exits) else float('inf')
            if next_entry_time < next_exit_time:
                self.current_locations[self.entries[self.entry_event_pointer][1]] = True
                self.entry_event_pointer += 1
            else:
                del self.current_locations[self.exits[self.exit_event_pointer][1]]
                self.exit_event_pointer += 1

        current_location = None
        if self.current_locations:
            # Pop off and append back on (peak is not supported).
            current_location, _ = self.current_locations.popitem()
            self.current_locations[current_location] = True
        return current_location

    def get_location(self, timestamp):

        # Perform binary search over entries, find most recent entry and exit.
        entry_index = self.previous_entry_index(timestamp)
        prev_exit_index = self.previous_exit_index(timestamp)

        # Work backwards finding most recent entry that hasn't been exited.
        if entry_index is None or entry_index == -1:
            return None
        if prev_exit_index is None or prev_exit_index == -1:
            return self.entries[entry_index][1]

        exit_history = set()
        exit_pointer = prev_exit_index
        while entry_index >= 0:
            entry_time, entry_region = self.entries[entry_index]
            while exit_pointer >= 0 and self.exits[exit_pointer][0] >= entry_time:
                exit_history.add(self.exits[exit_pointer][1])
                exit_pointer -= 1
            if entry_region not in exit_history:
                return entry_region
            entry_index -= 1
        return None

    def previous_entry_index(self, t):
        last_entry_index = self.__binary_search_movements(self.entries, t)
        if last_entry_index == len(self.entries):
            return last_entry_index - 1
        return last_entry_index

    def previous_exit_index(self, t):
        last_exit_index = self.__binary_search_movements(self.exits, t)
        if last_exit_index == len(self.exits):
            return last_exit_index - 1
        return last_exit_index

    @staticmethod
    def __binary_search_movements(movements, t):
        # Returns index of most recent historical movement, -1 if t is before first entry, len(movements) if after.

        if not movements:
            return None
        elif t < movements[0][0]:
            return -1
        elif t > movements[-1][0]:
            return len(movements)

        l = 0
        r = len(movements)
        while l < r:
            m = (l + r) // 2
            if movements[m][0] == t:
                return m
            elif movements[m][0] < t:
                l = m + 1
            elif movements[m][0] > t:
                r = m
        return l - 1


class Region:

    # Maintains state of movements at a particular region at an event.
    # Movements are of type [(timestamp, uuid, entered)], and are SORTED.
    # Entered is a boolean specifying if the region has been entered or exited.

    def __init__(self, region, movements=None):

        # Meta data.
        self.region = region

        # Movement data.
        self.movements = movements if movements is not None else []
        assert all([self.movements[i-1][0] <= self.movements[i][0] for i in range(1, len(self.movements))])

    def average_stay_time(self, start_time=0, end_time=float('inf')):
        # Calculates average time a person is in this region for between start_time (inclusive) and end_time
        # (exclusive), or for all records if these fields are not present.

        currently_present = {}
        times = [t for t, _, _ in self.movements]
        pointer = bisect.bisect_left(times, start_time)

        total_time = 0
        num_stays = 0

        while pointer < len(self.movements) and self.movements[pointer][0] < end_time:
            t, uid, entered = self.movements[pointer]
            if entered:
                currently_present[uid] = t
            elif uid in currently_present:
                # Case where the entrance was recorded during allotted time interval.
                entrance_time = currently_present[uid]
                num_stays += 1
                total_time += t - entrance_time
                del currently_present[uid]
            pointer += 1

        return float(total_time)/num_stays if num_stays != 0 else 0

    def bounce_rate(self, bounce_margin, start_time=0, end_time=float('inf')):
        # Calculates percentage of visitors to region, which leave the region in <= bounce_margin time.

        currently_present = {}
        times = [t for t, _, _ in self.movements]
        pointer = bisect.bisect_left(times, start_time)

        under_bounce_margin = 0
        over_bounce_margin = 0

        while pointer < len(self.movements) and self.movements[pointer][0] < end_time:
            t, uid, entered = self.movements[pointer]
            if entered:
                currently_present[uid] = t
            elif uid in currently_present:
                # Case where the entrance was recorded during allotted time interval.
                entrance_time = currently_present[uid]
                if t - entrance_time <= bounce_margin:
                    under_bounce_margin += 1
                else:
                    over_bounce_margin += 1
                del currently_present[uid]

            pointer += 1

        return float(under_bounce_margin)/(under_bounce_margin + over_bounce_margin) if under_bounce_margin != 0 else 0
