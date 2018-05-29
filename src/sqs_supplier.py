# -*- coding: utf-8 -*-

"""
The SQS Supplier's job is to push a new message onto the SQS queue at a specified interval (1 second or 1 minute)
with a new total correction at the given time, for the defined static position (latitude/longitude)

"""
import json
import time
import logging
from datetime import datetime
from threading import Thread

from tidegravity.tidegravity import solve_longman_tide_scalar as solve_tide


class SQSSupplier(Thread):
    def __init__(self, queue, lat, lon, alt, delay=60):
        super().__init__(name=__name__)
        self.queue = queue

        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.delay = delay
        self.log = logging.getLogger(__name__)
        self.log.debug("Queue URL: %s" % self.queue.url)
        self._start_delay = None

    def set_start_time(self, timestamp):
        pass

    @property
    def utctime(self):
        return datetime.utcnow()

    @property
    def timestamp(self):
        return time.time()

    def run(self):
        if self._start_delay:
            wait = self._start_delay + self.delay - self.timestamp
            self.log.debug("Sleeping for %.2f before starting." % wait)
            time.sleep(wait)

        while True:
            gm, gs, g0 = solve_tide(self.lat, self.lon, self.alt, self.utctime)
            message = {'Moon': gm, 'Sun': gs, 'total': g0, 'utctime': self.timestamp}
            res = self.queue.send_message(MessageBody=json.dumps(message),
                                          MessageGroupId='tide',
                                          MessageAttributes={
                                              'Latitude': {
                                                  'DataType': 'Number',
                                                  'StringValue': str(self.lat)
                                              },
                                              'Longitude': {
                                                  'DataType': 'Number',
                                                  'StringValue': str(self.lon)
                                              },
                                              'Altitude': {
                                                  'DataType': 'Number',
                                                  'StringValue': str(self.alt)
                                              }
                                          })
            time.sleep(self.delay)
