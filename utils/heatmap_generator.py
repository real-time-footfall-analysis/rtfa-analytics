from collections import defaultdict

from utils.person_tracker import PersonTracker


class HeatmapGenerator:

    # Maintains dict of people at an event, and can efficiently build position maps.

    def __init__(self, event_id, movements=None):

        # Meta data.
        self.event_id = event_id
        self.first_movement = None
        self.last_movement = None

        # Maps person_id -> person object.
        self.people = {}

        # Populate map if given movements.
        if movements is not None:

            # Filter by uid and append to people.
            for uid, timestamp, region, entered in movements:
                if uid not in self.people:
                    self.people[uid] = PersonTracker(uid)
                if entered:
                    self.people[uid].entries.append((timestamp, region))
                else:
                    self.people[uid].exits.append((timestamp, region))

            self.first_movement = movements[0][1]
            self.last_movement = movements[-1][1]

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
