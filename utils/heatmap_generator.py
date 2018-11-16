from collections import defaultdict

from utils.person_tracker import PersonTracker


class HeatmapGenerator:

    # Maintains dict of people at an event, and can efficiently build position maps.

    def __init__(self, event_id, movements=None, iterator_start_time=None):

        # Used to maintain state of previously generated heatmaps.
        self.historical_heatmaps = {}
        self.heatmap_times = []

        # Meta data.
        self.event_id = event_id
        self.first_movement = None
        self.last_movement = None

        # Maps person_id -> person object.
        self.people = {}

        # Populate map if given movements.
        if movements:

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

        self.generated_until = self.first_movement if iterator_start_time is None else iterator_start_time

        # Initialise people iterators.
        for person in self.people.values():
            person.initialise_location_iterator(self.generated_until)

    def append_movements(self, movements):
        if movements:
            if not self.people:
                self.first_movement = movements[0][1]

            for uid, timestamp, region, entered in movements:
                if uid not in self.people:
                    self.people[uid] = PersonTracker(uid)
                if entered:
                    self.people[uid].entries.append((timestamp, region))
                else:
                    self.people[uid].exits.append((timestamp, region))
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

    def build_heat_map_history(self, time_interval):
        # Efficiently iterates through people, adding their location data to a history of heatmaps at a given
        # time_interval.
        if self.last_movement is None:
            return [], {}

        end_time = self.last_movement
        time = self.generated_until
        while time <= end_time:
            time += time_interval
            if time not in self.historical_heatmaps:
                self.historical_heatmaps[str(time)] = {}
                self.heatmap_times.append(time)
            for person in self.people.values():
                location = person.get_next_location(time_interval)
                if location is not None:
                    self.historical_heatmaps[str(time)][str(location)] \
                        = self.historical_heatmaps[str(time)].get(str(location), 0) + 1

        # Record time of last generation.
        self.generated_until = self.last_movement

        # Clear movement cache in people.
        for person in self.people.values():
            person.clear_movement_cache()

        return self.heatmap_times, self.historical_heatmaps
