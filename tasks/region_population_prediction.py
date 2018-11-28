import math
import time

from tasks.task import Task
from utils.heatmap_generator import HeatmapGenerator
from utils.region_population_predictor import RegionPopulationPredictor


class RegionPopulationPrediction(Task):
    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        state_package = self.state_data.get_task_state(self.task_id, event_id)
        if state_package is not None:
            # Get all movements since last movement, not including what has occurred in the current second.
            heatmap_gen, predictor = state_package
            last_movement = heatmap_gen.last_movement if heatmap_gen.last_movement else -1
            movements_since_last_update = self.log_source.retrieve_event_movements(event_id, time_start=last_movement+1,
                                                                                   time_end=math.floor(time.time()))
            heatmap_gen.append_movements(movements_since_last_update)
        else:
            event_movements = self.log_source.retrieve_event_movements(event_id)
            heatmap_gen = HeatmapGenerator(event_id, event_movements)
            predictor = RegionPopulationPredictor()

        heatmaps = heatmap_gen.build_heat_map_history(100)[1]
        for timestamp, heatmap in heatmaps.items():
            predictor.add_heat_table(int(timestamp), heatmap)

        result = predictor.calculate_average_region_population_by_30_min_buckets()

        heatmap_gen.historical_heatmaps = {}
        heatmap_gen.heatmap_times = []
        state_package = (heatmap_gen, predictor)
        self.state_data.save_task_state(self.task_id, event_id, state_package)

        return result
