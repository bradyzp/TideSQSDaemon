TideSQSDaemon
=============

A simple Python service designed to be run as a daemon, it will compute tidal gravity corrections (Sun/Moon/Total)
based on the given Lat/Lon/Alt and the current time, then push the data to an AWS SQS (Simple Queue Service) Queue for
consumption by another service.


Requirements
------------

- tidegravity
- boto3
