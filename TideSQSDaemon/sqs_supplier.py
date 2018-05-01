# -*- coding: utf-8 -*-

"""
The SQS Supplier's job is to push a new message onto the SQS queue at a specified interval (1 second or 1 minute)
with a new total correction at the given time, for the defined static position (latitude/longitude)

"""
import json
import time
from datetime import datetime
from threading import Thread

import boto3
from tidegravity.tidegravity import solve_longman_tide_scalar as solve_tide


class SQSSupplier(Thread):
    def __init__(self, lat, lon, alt, delay=60, aws_profile='default'):
        super().__init__(name=__name__)
        session = boto3.Session(profile_name=aws_profile)
        sqs = session.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName='tide-gravity-queue')
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.delay = delay

    @property
    def ctime(self):
        return datetime.utcnow()

    def run(self):
        while True:
            ctime = self.ctime
            gm, gs, g0 = solve_tide(self.lat, self.lon, self.alt, ctime)
            message = {'Moon': gm, 'Sun': gs, 'Total': g0}
            self.queue.send_message(MessageBody=json.dumps(message),
                                    MessageAttributes={
                                        'Latitude': {
                                            'DataType': 'Number',
                                            'StringValue': str(self.lat)
                                        },
                                        'Longitude': {
                                            'DataType': 'Number',
                                            'StringValue': str(self.lon)
                                        },
                                        'UTCTime': {
                                            'DataType': 'Number',
                                            'StringValue': str(self.ctime.timestamp())
                                        }
                                    })
            time.sleep(self.delay)
