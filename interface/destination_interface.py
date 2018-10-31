from typing import Dict
import decimal
from interface.log_interface import LogInterface
import logging
import sys
import boto3

class DestinationInterface:

    def __init__(self):

        self.config = {
            'region': 'eu-central-1',
            'dynamo_endpoint': 'https://dynamodb.eu-central-1.amazonaws.com',
            'dynamo_table': 'analytics_results'
        }

        self.__dynamodb = boto3.resource('dynamodb', region_name=self.config['region'], endpoint_url=self.config['dynamo_endpoint'])
        self.__table = self.__dynamodb.Table(self.config['dynamo_table'])
        self.__logger = logging.StreamHandler(sys.stdout)

    # Credit: https://stackoverflow.com/a/50815499/3837124
    def rec_map(self, it, f):
        if isinstance(it, dict):
            acc = {}
            for key, value in it.items():
                acc[key] = self.rec_map(value, f)
            return acc

        elif isinstance(it, (list, tuple, set)):
            acc = []
            for item in it:
                acc.append(self.rec_map(item, f))
            return type(it)(acc)

        else:
            return f(it)

    # Conversion between python and dynamodb types
    def conv_to_dynodb_types(self, item):
        if isinstance(item, float):
            return decimal.Decimal(str(item))
        else:
            return item

    def update_object(self, task_id, event_id, json_obj: Dict):
        try:
            dynamo_item = self.rec_map(json_obj, self.conv_to_dynodb_types)
            dynamo_item["EventID-TaskID"] = "%d-%d" % (event_id, task_id)

            response = self.__table.put_item(
                Item=dynamo_item
            )

            respCode = response["ResponseMetadata"]["HTTPStatusCode"]
            if respCode != 200:
                raise Exception("Response code " + str(respCode) + " from AWS")
            
        except Exception as e:
            self.__logger.handleError("Failed to write to DynamoDB: " + str(e))
