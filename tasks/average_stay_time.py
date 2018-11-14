from tasks.task import Task
from utils.region_tracker import RegionTracker


class AverageStayTime(Task):
    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        event_movements = self.log_source.retrieve_event_movements(event_id)
        regionTrackers = {}

        # Get list of regions from RDS Static event DB
        regions = self.static_data_source.get_regions(event_id)

        # Populate regionTrackers list with all regions that have the "queue" TAG
        for id in regions:
            regionTrackers[id] = RegionTracker(id)

        for uid, timestamp, region, entered in event_movements:
            if region in regionTrackers:
                regionTrackers[region].movements.append((timestamp, uid, entered))

        stay_times = {}

        for region in regionTrackers:
            stay_times[str(region)] = regionTrackers[region].average_stay_time()

        return stay_times