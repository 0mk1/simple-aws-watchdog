# aws-watchdog

### Installation

Remember that aws_watchdog is working on Python 3+.

If on system is python 2 and 3, then change `pip` to `pip3`.


Install aws_watchdog on user that have permissions to systemctl restart and 
status commands, and also have access to /var/log/.

TODO: create script that create aws_watchdog user in system.

#### PyPi

```bash
pip install https://bitbucket.org/toffi9/aws-watchdog/get/master.zip#egg=aws_watchdog-0.0.1
```
#### Manual

```
git clone git@bitbucket.org:toffi9/aws-watchdog.git
pip install -r requirements.txt
```

### Usage

```bash
aws_watchdogd --help
aws_watchdogd --config-id (INTEGER, default=1)
```

`config-id` is ID of row in DynamoDB from which daemon has to download config
