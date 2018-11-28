from tasks.average_queue_time import AverageQueueTime
from tasks.average_stay_time import AverageStayTime
from tasks.bounce_rate import BounceRate
from tasks.historical_heatmaps import HistoricalHeatmaps
from tasks.region_population_prediction import RegionPopulationPrediction

# Maps task ids to task definitions, used to find enabled tasks for a particular event,
TASK_IDS = {
    1: AverageStayTime,
    2: BounceRate,
    3: AverageQueueTime,
    4: HistoricalHeatmaps,
    5: RegionPopulationPrediction,
}

# Maps frequency groups to set of task_ids to be executed at particular frequency.
FREQUENCY_GROUPS = {
    5: {1, 2, 3, 4, 5},
}