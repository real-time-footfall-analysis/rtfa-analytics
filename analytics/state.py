from operator import itemgetter


class Person:

    # Maintains state of a single persons location throughout event.
    # Movements are of type [(timestamp, region, entered)], and are SORTED.
    # Entered is a boolean specifying if the region has been entered or exited.

    def __init__(self, movements=None):

        self.entries, self.exits = [], []

        if movements is not None:
            movements.sort(key=itemgetter(0))
            for (timestamp, region, entered) in movements:
                if entered:
                    self.entries.append((timestamp, region))
                else:
                    self.exits.append((timestamp, region))

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
