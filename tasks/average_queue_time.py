from interface.log_interface import LogInterface
from interface.static_data_interface import StaticDataInterface
from utils.region_tracker import RegionTracker
import json


def average_queue_time(log_source: LogInterface, static_data_source: StaticDataInterface, event_id):
    event_movements = log_source.retrieve_event_movements(event_id)
    regionTrackers = {}

    # Get list of regions from RDS Static event DB
    regions = static_data_source.get_region_attributes(event_id, "is_queue")

    # Populate regionTrackers list with all regions that have the "queue" TAG
    for id, is_queue in regions.items():
        if is_queue:
            regionTrackers[id] = RegionTracker(id)

    for uid, timestamp, region, entered in event_movements:
        if region in regionTrackers:
            regionTrackers[region].movements.append((timestamp, uid, entered))

    stay_times = []

    for region in regionTrackers:
        stay_times.append({"id": region, "waitTime": regionTrackers[region].average_stay_time()})

    return stay_times
