from mock import patch

from handler.request_handler import RequestHandler


def test_average_stay_time_basic():
    with \
            patch('interface.state_interface.StateInterface') as state_interface, \
            patch('interface.static_data_interface.StaticDataInterface') as static_data_interface, \
            patch('interface.log_interface.LogInterface') as log_interface, \
            patch('interface.destination_interface.DestinationInterface') as dest_interface:
        # Patch methods.
        static_data_interface.get_running_events.return_value = {0}
        static_data_interface.get_regions.return_value = {1}
        static_data_interface.get_enabled_tasks.return_value = {1}
        log_interface.retrieve_event_movements.return_value = [("uuid", 392, 1, True), ("uuid", 399, 1, False)]

        # Initialise handler.
        handler = RequestHandler(state_data=state_interface, static_data_source=static_data_interface,
                                 log_source=log_interface, data_dest=dest_interface)
        handler.execute_tasks(5)
        dest_interface.update_object.assert_called_once_with(1, 0, {'1': 7.0})
