from tasks.task import Task
from utils.region_tracker import RegionTracker


class BounceRate(Task):
    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        event_movements = self.log_source.retrieve_event_movements(event_id)

        region_trackers = {}
        for uid, timestamp, region, entered in event_movements:
            if region not in region_trackers:
                region_trackers[region] = RegionTracker(region)
            region_trackers[region].movements.append((timestamp, uid, entered))

        region_thresholds = self.static_data_source.get_region_attributes(event_id, "bounce_rate_threshold")

        bounce_rates = {}
        for region in region_trackers:
            threshold = region_thresholds[region]
            bounce_rate = region_trackers[region].bounce_rate(threshold)
            bounce_rates[str(region)] = {"bounceRate": bounce_rate, "threshold": threshold}

        return bounce_rates
