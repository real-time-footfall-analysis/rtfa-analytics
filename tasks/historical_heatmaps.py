from tasks.task import Task
from utils.heatmap_generator import HeatmapGenerator


class HistoricalHeatmaps(Task):
    def __init__(self, state_data, log_source, static_data_source, task_id):
        super().__init__(state_data, log_source, static_data_source, task_id)

    def execute(self, event_id):
        event_movements = self.log_source.retrieve_event_movements(event_id)
        heatmap_gen = HeatmapGenerator(event_id, event_movements)
        times, heatmaps = heatmap_gen.build_heat_map_history(time_interval=100)
        result = {"timestamps": times, "data": heatmaps}
        return result