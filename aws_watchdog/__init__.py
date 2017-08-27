import logging
import time

from .config import DynamoDBConfig
from .notifications import SNS
from .utils import (
    is_service_running,
    restart_service,
)


__all__ = ['aws_watchdog']


logger = logging.getLogger(__name__)


def aws_watchdog(config_id):
    """AWS watchdog function. Health check for your services."""
    # TODO: checking config every 15minutes

    config = DynamoDBConfig('mkamycki-watchdog-table', config_id)
    notification_module = SNS(
        'arn:aws:sns:us-west-2:632826021673:mkamycki-watchdog-topic'
    )

    while True:
        for service in config.list_of_services:

            if not is_service_running(service):
                service_down_message = '{} is down.'.format(service)
                logger.error(service_down_message)
                notification_module.publish(service_down_message)

                for attempt in range(1, config.num_of_attempts + 1):

                    logger.info(
                        'Restarting {}. Attempt {}'.format(service, attempt)
                    )
                    restart_command_exit_code = restart_service(service)

                    if restart_command_exit_code == 0:
                        success_restart_message = (
                            'Success of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                        logger.info(success_restart_message)
                        notification_module.publish(success_restart_message)
                        break

                    if attempt == config.num_of_attempts:
                        failure_restart_message = (
                            'Failure of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                        logger.error(failure_restart_message)
                        notification_module.publish(failure_restart_message)

                    time.sleep(config.num_of_sec_wait)

        time.sleep(config.num_of_sec_check)
