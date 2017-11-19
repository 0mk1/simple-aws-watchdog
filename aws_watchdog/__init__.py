import logging
import time
from datetime import datetime, timedelta

from .config import DynamoDBConfig
from .notifications import SNS
from .utils import check_and_heal_service


__all__ = ['aws_watchdog']


logger = logging.getLogger(__name__)


def aws_watchdog(config_id):
    """AWS watchdog function. Health check for your services."""

    # TODO: sns topic arn
    notification_module = SNS()

    # TODO: dynamodb table
    config = DynamoDBConfig('', config_id)
    start_time = datetime.now()

    while True:
        if (datetime.now() - start_time) >= timedelta(minutes=15):
            # reloading config
            # TODO: dynamodb table
            config = DynamoDBConfig('', config_id)
            start_time = datetime.now()

        for service in config.list_of_services:
            check_and_heal_service(
                service,
                config.num_of_attempts,
                config.num_of_sec_wait,
                notification_module,
            )
        time.sleep(config.num_of_sec_check)
