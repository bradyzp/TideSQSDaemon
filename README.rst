TideSQSDaemon
=============

A simple Python service designed to be run as a daemon, it will compute tidal gravity corrections (Sun/Moon/Total)
based on the given Lat/Lon/Alt and the current time, then push the data to an AWS SQS (Simple Queue Service) Queue for
consumption by another service.


Requirements
------------

- tidegravity
- boto3


Installation
------------

ToDo: PyPi distribution and installation instruction

An example Systemd service unit file is provided which can be used to install this daemon as a service on a Linux system
using systemd. Simply change the parameter values as required.
The TideSQS.service file should then be copied/moved to /etc/systemd/system/TideSQS.service
Run the following commands after installing the service file to the location above:

```
systemctl daemon-reload
systemctl enable TideSQS.service
systemctl start TideSQS.service

```


Note: An aws credentials file must also be created with appropriate API access keys for the daemon to write to an AWS
SQS queue.
