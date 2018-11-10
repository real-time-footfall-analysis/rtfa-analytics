from tasks.Task import Task
from utils.region_tracker import RegionTracker


class AverageQueueTime(Task):

    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        event_movements = self.log_source.retrieve_event_movements(event_id)
        region_trackers = {}

        # Get list of regions from RDS Static event DB
        regions = self.static_data_source.get_region_attributes(event_id, "is_queue")

        # Populate region_trackers list with all regions that have the "queue" TAG
        for id, is_queue in regions.items():
            if is_queue:
                region_trackers[id] = RegionTracker(id)

        for uid, timestamp, region, entered in event_movements:
            if region in region_trackers:
                region_trackers[region].movements.append((timestamp, uid, entered))

        stay_times = []

        for region in region_trackers:
            stay_times.append({"id": region, "waitTime": region_trackers[region].average_stay_time()})

        return stay_times
