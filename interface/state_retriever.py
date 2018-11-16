import decimal
import logging

import boto3
import pickle

import sys

from interface.state_interface import StateInterface


class StateRetriever(StateInterface):

    def __init__(self):
        super().__init__()

        self.config = {
            'region': 'eu-central-1',
            'dynamo_endpoint': 'https://dynamodb.eu-central-1.amazonaws.com',
            'dynamo_table': 'analytics_state'
        }

        self.__dynamodb = boto3.resource('dynamodb', region_name=self.config['region'],
                                         endpoint_url=self.config['dynamo_endpoint'])
        self.__table = self.__dynamodb.Table(self.config['dynamo_table'])
        self.__logger = logging.StreamHandler(sys.stdout)

    def __rec_map(self, it, f):
        if isinstance(it, dict):
            acc = {}
            for key, value in it.items():
                acc[key] = self.__rec_map(value, f)
            return acc

        elif isinstance(it, (list, tuple, set)):
            acc = []
            for item in it:
                acc.append(self.__rec_map(item, f))
            return type(it)(acc)

        else:
            return f(it)

    # Conversion between python and dynamodb types
    def __conv_to_dynodb_types(self, item):
        if isinstance(item, float):
            return decimal.Decimal(str(item))
        else:
            return item

    def __update_object(self, task_id, event_id, state):

        pickled_state = pickle.dumps(state)

        # Wrap object in result dict.
        obj_to_store = {"result": pickled_state}

        try:
            dynamo_item = self.__rec_map(obj_to_store, self.__conv_to_dynodb_types)
            dynamo_item["EventID-TaskID"] = "%d-%d" % (event_id, task_id)

            response = self.__table.put_item(
                Item=dynamo_item
            )

            respCode = response["ResponseMetadata"]["HTTPStatusCode"]
            if respCode != 200:
                raise Exception("Response code " + str(respCode) + " from AWS")

        except Exception as e:
            self.__logger.handleError("Failed to write to DynamoDB: " + str(e))

    def __retrieve_object(self, task_id, event_id):
        response = self.__table.get_item(
            Key={"EventID-TaskID": "%d-%d" % (event_id, task_id)}
        )
        try:
            return response['Item']['result'].value
        except KeyError:
            return None

    def save_task_state(self, task_id, event_id, state):
        self.__update_object(task_id, event_id, state)

    def get_task_state(self, task_id, event_id):
        binary_object = self.__retrieve_object(task_id, event_id)
        return pickle.loads(binary_object) if binary_object is not None else None
