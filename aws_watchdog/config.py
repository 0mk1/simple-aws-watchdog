import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class DynamoDBConfig:

    def __init__(self, table_name, config_id):
        self.table_name = table_name
        self.client = boto3.client('dynamodb')
        self._raw_config = self.get_raw_config(config_id)
        logger.info(self._raw_config)

        self.list_of_services = self.get_list_of_services()
        self.num_of_sec_check = self.get_num_of_sec_check()
        self.num_of_sec_wait = self.get_num_of_sec_wait()
        self.num_of_attempts = self.get_num_of_attempts()

    def get_raw_config(self, config_id):
        try:
            return self.client.get_item(
                TableName=self.table_name,
                Key={
                    'id': {
                        'S': str(config_id),
                    },
                },
            )
        except ClientError as err:
            logger.error(err)
            raise err

    def get_list_of_services(self):
        item = self.get_item_from_raw_config()
        services_list = item['ListOfServices']['L']

        return [service_dict['S'] for service_dict in services_list]

    def get_num_of_sec_check(self):
        item = self.get_item_from_raw_config()
        return int(item['NumOfSecCheck']['N'])

    def get_num_of_sec_wait(self):
        item = self.get_item_from_raw_config()
        return int(item['NumOfSecWait']['N'])

    def get_num_of_attempts(self):
        item = self.get_item_from_raw_config()
        return int(item['NumOfAttempts']['N'])

    def get_item_from_raw_config(self):
        raw_config = self._raw_config
        return raw_config['Item']
