import logging
import time

import click

from .config import DynamoDBConfig
from .utils import (
    current_user_is_root,
    is_service_running,
    restart_service,
)


__all__ = ['aws_watchdog', 'aws_watchdog_daemon']


logger = logging.getLogger(__name__)


def aws_watchdog(config_id):
    """AWS watchdog function. Health check for your services."""
    # TODO: each service checks should be in different process to do thins in
    # parallel and get proper waithing times. use multiprocessing
    # TODO: consider selfhealing of aws_watchdog
    # TODO: systemd service

    config = DynamoDBConfig(config_id)

    while True:
        for service in config.list_of_services:

            if not is_service_running(service):
                logger.error('{} is down.'.format(service))

                for attempt in range(1, config.num_of_attempts + 1):
                    logger.info(
                        'Restarting {}. Attempt {}'.format(service, attempt)
                    )
                    restart_command_exit_code = restart_service(service)
                    if restart_command_exit_code == 0:
                        logger.info(
                            'Success of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                        break
                    if attempt == config.num_of_attempts:
                        logger.error(
                            'Failure of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                    time.sleep(config.num_of_sec_wait)

        time.sleep(config.num_of_sec_check)


@click.command()
@click.option(
    '--config-id',
    default=1,
    help='ID of config entry in DynamoDB (default is 1)',
)
def aws_watchdog_daemon(config_id):
    # TODO: user can choose where to log
    logger.info(
        'Starting AWS watchdog daemon. (PID )'.format()
    )
    if current_user_is_root():
        logger.warn('Running things as root can be dangerous !!')

    aws_watchdog(config_id)
