import getpass
import logging
import subprocess


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
