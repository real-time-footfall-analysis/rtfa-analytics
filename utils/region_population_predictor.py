from collections import defaultdict


class RegionPopulationPredictor:
    def __init__(self):
        self.accumulated_populations_by_30_mins_by_region = {}
        self.num_samples_by_30_min_bucket = defaultdict(int)
        self.max_per_region = defaultdict(int)

    def add_heat_table(self, time_of_table, table):

        # Round down time_of_table to nearest multiple of 30 mins, then mod by 24 hours.
        time_of_table = (time_of_table - (time_of_table % 1800)) % 86400

        self.num_samples_by_30_min_bucket[time_of_table] += 1

        if time_of_table not in self.accumulated_populations_by_30_mins_by_region:
            self.accumulated_populations_by_30_mins_by_region[time_of_table] = defaultdict(int)

        for region in table:
            self.accumulated_populations_by_30_mins_by_region[time_of_table][region] += table[region]
            self.max_per_region[region] = max(self.max_per_region[region], table[region])

    def calculate_average_region_population_by_30_min_buckets(self):
        ratios = {}
        counts = {}
        for time in self.accumulated_populations_by_30_mins_by_region:
            regions = self.accumulated_populations_by_30_mins_by_region[time]
            for region in regions:
                if region not in counts:
                    counts[str(region)] = {}
                    ratios[str(region)] = {}
                counts[str(region)][str(time)] = regions[region]//self.num_samples_by_30_min_bucket[time]
                ratios[str(region)][str(time)] = counts[str(region)][str(time)] / self.max_per_region[region]

        return {"counts": counts, "ratios": ratios}