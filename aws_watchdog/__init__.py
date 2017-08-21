import click
# import daemon
import logging
import logging.config
import time
import os
import subprocess


__version__ = '0.0.1'


logger = logging.getLogger(__name__)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/aws_watchdog.log',
            'when': 'm',
            'interval': 10,
            'backupCount': 10,
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
})


def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0


def try_to_restart(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'restart'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0


@click.command()
@click.option(
    '--config-id',
    default=1,
    help='ID of config entry in DynamoDB (default is 1)',
)
def aws_watchdog_daemon(config_id):
    """AWS watchdog daemon. Health check for your services."""

    # with daemon.DaemonContext() as dmon:
    starting_message = 'Starting AWS watchdog daemon. (PID )'.format(
        # dmon.pid,
    )
    print(starting_message)
    logger.info(starting_message)

    while True:
        # TODO: If working then 'already run'
        if not is_service_running('docker'):
            logger.error('Docker not working !!!')
            try_to_restart('docker')

        if is_service_running('docker'):
            logger.error('Docker working !!!')
        time.sleep(1)

# TODO: checking every Y seconds if X services is running (status: active)
# TODO: if down then try to start it N seconds M times

# TODO: store configs in cache, if changed remote every 15minutes check, then update cache
# TODO: validation configs saved in DynamoDB
# TODO: log the events: service is down, number of start attempts and results
# TODO: logging to S3
# TODO: AWS SNS email when: service down, success started after Z attempts, failture after Z attempts
# TODO: write installation by pip guide in README
