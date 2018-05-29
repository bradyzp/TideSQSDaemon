# -*- coding: utf-8 -*-

import json
import logging

from tidegravity import tidegravity as tide


class SQSGenerator:
    def __init__(self, queue, lat, lon, alt):
        self.queue = queue
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self._data = []
        self.log = logging.getLogger(__name__)

    def purge(self, silently_continue=True):
        try:
            self.queue.purge()
        except:
            # Expect a botocore.errorfactory.PurgeQueueInProgress exception (don't know where to source this from)
            # This happens if purge is called more than once every 60 seconds
            self.log.exception("Exception purging queue.")
            if not silently_continue:
                raise

    def _form_mesage(self, body, gid, msg_id=None):
        msg = dict(MessageBody=json.dumps(body),
                   MessageGroupId=gid,
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
                       },
                   }
                   )
        if msg_id is not None:
            # Used for batch sending messages, must be unique for each message within a batch
            msg['Id'] = str(msg_id)
        return msg

    def _send(self, body, gid='tide'):
        self.queue.send_message(self._form_mesage(body, gid))

    def batch_send(self, purge=False):
        if purge:
            self.purge()
        max_batch = 10
        for i in range(len(self._data) // max_batch):
            idx = i * max_batch
            selection = self._data[idx:idx+max_batch]
            messages = [self._form_mesage(body, 'tide', msg_id=mid) for mid, body in enumerate(selection)]
            result = self.queue.send_messages(Entries=messages)
            self.log.debug(result)

    def enqueue(self, purge=False):
        if purge:
            self.purge()

        self.log.info("Sending messages to queue")
        for message in self._data:
            self._send(message)

        self.log.info("Done")

    def generate(self, n, start, increment):
        """Generate Tide/Time dicts and enqueue them on a local queue to be sent"""
        df = tide.solve_point_corr(self.lat, self.lon, self.alt, t0=start, n=n, increment=increment)
        for i, line in df.iterrows():
            self._data.append(dict(total=line['total_corr'], utctime=line.name.timestamp()))

        return self._data
