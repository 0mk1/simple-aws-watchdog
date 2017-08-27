import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SNS:

    def __init__(self, topic_arn):
        self.topic_arn = topic_arn
        self.client = boto3.client('sns')

    def publish(self, message, subject='AWS Watchdog'):
        try:
            response = self.client.publish(
                TopicArn=self.topic_arn,
                Message=message,
                Subject=subject,
                MessageStructure='string',
            )
            logger.info(response)
        except ClientError as err:
            logger.error(err)
            raise err
