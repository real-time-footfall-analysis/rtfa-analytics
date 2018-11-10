from interface.log_interface import LogInterface
from interface.static_data_interface import StaticDataInterface
from utils.region_tracker import RegionTracker


def bounce_rate(log_source: LogInterface, static_data_source: StaticDataInterface, event_id):
    event_movements = log_source.retrieve_event_movements(event_id)

    region_trackers = {}
    for uid, timestamp, region, entered in event_movements:
        if region not in region_trackers:
            region_trackers[region] = RegionTracker(region)
        region_trackers[region].movements.append((timestamp, uid, entered))

    region_thresholds = static_data_source.get_region_attributes(event_id, "bounce_rate_threshold")

    bounce_rates = {}
    for region in region_trackers:
        threshold = region_thresholds[region]
        bounce_rate = region_trackers[region].bounce_rate(threshold)
        bounce_rates[str(region)] = {"bounceRate": bounce_rate, "threshold": threshold}

    return bounce_rates
