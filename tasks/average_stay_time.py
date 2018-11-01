from interface.log_interface import LogInterface
from interface.static_data_interface import StaticDataInterface
from utils.region_tracker import RegionTracker
import json


def average_stay_time(log_source: LogInterface, static_data_source: StaticDataInterface, event_id):
    event_movements = log_source.retrieve_event_movements(event_id)
    regionTrackers = {}

    # Get list of regions from RDS Static event DB
    regions = static_data_source.get_regions(event_id)

    # Populate regionTrackers list with all regions that have the "queue" TAG
    for id, _ in regions:
        regionTrackers[id] = RegionTracker(id)

    for uid, timestamp, region, entered in event_movements:
        if region in regionTrackers:
            regionTrackers[region].movements.append((timestamp, uid, entered))

    stay_times = {}

    for region in regionTrackers:
        stay_times[str(region)] = regionTrackers[region].average_stay_time()
    obj_to_store = {'result': stay_times}

    return obj_to_store