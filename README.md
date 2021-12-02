# Nagiode

Nagiode is a lightweight nagios cli written in python3. 

## Installation

```
git clone https://github.com/afrank/nagiode
cd nagiode
pip3 install .
```

## Usage

```
$ nagiode -h
usage: nagiode [-h] [-c COMMAND] [-l] [-a ARG] [-H HOST] [-U USERNAME] [-P PASSWORD] [-s] [-G CGI] [-d]

Nagiode v0.1

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Nagios Command to use. Use -l to list available commands
  -l, --list            List available commands. If used with -c list arguments for command.
  -a ARG, --arg ARG
  -H HOST, --host HOST  Nagios Host
  -U USERNAME, --username USERNAME
                        Nagios Username
  -P PASSWORD, --password PASSWORD
                        Nagios Password
  -s, --status          Get Host status. Requires -a host=<host>
  -G CGI, --cgi CGI     Nagios CGI Path
  -d, --debug           Print url and args and exit without executing
```

Nagiode supports environment variables for credentials so you don't need to bake creds into scripts. The variables are:

```
NAGIOS_HOST: hostname for nagios without proto
NAGIOS_USER: your username for logging into nagios
NAGIOS_PASS: your password for logging into nagios
```

You can list all available commands in nagiode with `-l`:
```
$ nagiode -l
["CMD_ADD_HOST_COMMENT", "CMD_ACKNOWLEDGE_HOST_PROBLEM", "CMD_ADD_SVC_COMMENT", "CMD_ACKNOWLEDGE_SVC_PROBLEM", "CMD_DISABLE_SVC_CHECK", "CMD_ENABLE_SVC_CHECK", "CMD_DISABLE_SVC_NOTIFICATIONS", "CMD_ENABLE_SVC_NOTIFICATIONS", "CMD_SCHEDULE_SVC_DOWNTIME", "CMD_SCHEDULE_HOST_DOWNTIME", "CMD_DISABLE_HOST_SVC_NOTIFICATIONS", "ENABLE_HOST_SVC_NOTIFICATIONS", "CMD_PROCESS_SERVICE_CHECK_RESULT", "CMD_SCHEDULE_SVC_CHECK"]
```

If you use `-l` with a command, nagiode will print all the required arguments for that command:
```
$ nagiode -c CMD_SCHEDULE_SVC_DOWNTIME -l
["host", "service", "com_author", "com_data", "fixed", "start_time", "end_time"]
```

The `-a` argument can be supplied multiple times with different command arguments:
```
$ nagiode -c CMD_SCHEDULE_SVC_DOWNTIME -a host=myhost -a service=swap -a "com_data=scheduling downtime for swap check"
Your command request was successfully submitted to Nagios for processing.
Note: It may take a while before the command is actually processed.
Done
```

If you supply `-s` with no command for a host nagiode will return the current service status of that host in json:
```
$ nagiode -s -a host=myhost | jq . | head -25
{
  "RAID": {
    "last_check": "2021-04-14 15:48:02",
    "duration": "569d 15h 55m 30s",
    "attempt": "1/2",
    "status": "OK"
  },
  "fs_space": {
    "last_check": "2021-04-14 15:48:02",
    "duration": "510d 21h 58m  3s",
    "attempt": "1/1",
    "status": "10.45"
  },
  "network": {
    "last_check": "2021-04-14 15:45:08",
    "duration": "198d  2h 54m 12s",
    "attempt": "1/1",
    "status": "OK"
  },
```

