import bisect


class RegionTracker:

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