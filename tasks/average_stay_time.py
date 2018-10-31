from interface.log_interface import LogInterface
from utils.region_tracker import RegionTracker


def average_stay_time(log_source: LogInterface, event_id):
    event_movements = log_source.retrieve_event_movements(event_id)
    regions = {}
    for uid, timestamp, region, entered in event_movements:
        if region not in regions:
            regions[region] = RegionTracker(region)
        regions[region].movements.append((timestamp, uid, entered))

    stay_times = {}
    for region in regions:
        stay_times[str(region)] = regions[region].average_stay_time()

    obj_to_store = {'result': stay_times}

    return obj_to_store
