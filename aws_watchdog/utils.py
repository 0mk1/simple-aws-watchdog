import getpass
import logging
import subprocess
import time


logger = logging.getLogger(__name__)


def run_command(command_list):
    """Run shell command in subprocess.

    Returns exit code of commmand. Suppressing any stdout and stderr.
    """
    try:
        proc = subprocess.Popen(
            command_list,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        exit_code = proc.wait()
        return exit_code
    except (OSError, subprocess.CalledProcessError) as err:
        logger.error(err)
        raise err


def is_service_running(name):
    """Check if service is running on linux system.

    Need to use system with systemd.
    """
    exit_code = run_command(['systemctl', 'status', name])
    return exit_code == 0


def restart_service(name):
    """Restart service on linux system.

    Need to use system with systemd.
    Returns exit code of restarting command.
    """
    exit_code = run_command(['systemctl', 'restart', name])
    return exit_code


def current_user_is_root():
    return getpass.getuser() == 'root'


def check_and_heal_service(
        service,
        num_of_attempts,
        num_of_sec_wait,
        notification_module
):
    if not is_service_running(service):
        service_down_message = '{} is down.'.format(service)
        logger.error(service_down_message)
        notification_module.publish(service_down_message)

        for attempt in range(1, num_of_attempts + 1):

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

            if attempt == num_of_attempts:
                failure_restart_message = (
                    'Failure of restarting {}. On {} attempt.'.format(
                        service,
                        attempt,
                    )
                )
                logger.error(failure_restart_message)
                notification_module.publish(failure_restart_message)

            time.sleep(num_of_sec_wait)
