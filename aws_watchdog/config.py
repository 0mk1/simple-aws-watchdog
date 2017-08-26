import boto3


class DynamoDBConfig:

    # TODO: do it more flexible
    table_name = 'mkamycki-watchdog-table'

    # TODO: every 15minutes reload config

    def __init__(self, config_id):
        self.client = boto3.client('dynamodb')
        self._raw_config = self.get_raw_config(config_id)
        print(self._raw_config)

        self.list_of_services = self.get_list_of_services()
        self.num_of_sec_check = self.get_num_of_sec_check()
        self.num_of_sec_wait = self.get_num_of_sec_wait()
        self.num_of_attempts = self.get_num_of_attempts()

    def get_raw_config(self, config_id):
        return self.client.get_item(
            TableName=self.table_name,
            # Key={
            #     'string': {
            #         'S': 'string',
            #         'N': 'string',
            #         'B': b'bytes',
            #         'SS': [
            #             'string',
            #         ],
            #         'NS': [
            #             'string',
            #         ],
            #         'BS': [
            #             b'bytes',
            #         ],
            #         'M': {
            #             'string': {'... recursive ...'}
            #         },
            #         'L': [
            #             {'... recursive ...'},
            #         ],
            #         'NULL': True|False,
            #         'BOOL': True|False
            #     }
            # },
            # AttributesToGet=[
            #     'string',
            # ],
            # ConsistentRead=True|False,
            # ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
            # ProjectionExpression='string',
            # ExpressionAttributeNames={
            #     'string': 'string'
            # }
        )

    def get_list_of_services(self):
        # TODO: validation
        return ['ufw', 'docker']

    def get_num_of_sec_check(self):
        # TODO: validation
        return 5

    def get_num_of_sec_wait(self):
        # TODO: validation
        return 5

    def get_num_of_attempts(self):
        # TODO: validation
        return 4
