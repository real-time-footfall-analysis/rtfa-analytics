from mock import patch

from handler.request_handler import RequestHandler


def test_average_stay_time_basic():
    with patch('interface.static_data_interface.StaticDataInterface') as static_data_interface, \
            patch('interface.log_interface.LogInterface') as log_interface, \
            patch('interface.destination_interface.DestinationInterface') as dest_interface:
        # Patch methods.
        static_data_interface.get_running_events.return_value = {0}
        static_data_interface.get_enabled_tasks.return_value = {1}
        log_interface.retrieve_event_movements.return_value = [(1, 392, 'a', True), (1, 399, 'a', False)]

        # Initialise handler.
        handler = RequestHandler(static_data_source=static_data_interface, log_source=log_interface,
                                 data_dest=dest_interface)
        handler.execute_tasks(5)
        dest_interface.update_object.assert_called_once_with(1, 0, {'a': 7.0})
