# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import time
import threading
import queue
import tidegravity as tide


def point_correction(lat, lon, alt=0, date=datetime.utcnow()):
    """Solve tidal correction for a static point and time"""
    gm, gs, g0 = tide.solve_longman_tide_scalar(lat, lon, alt, date)
    message = {'gm': gm, 'gs': gs, 'g0': g0, 'ts': date.timestamp()}
    return message


def series_correction(lat, lon, alt=0, date=datetime.now(tz=timezone.utc), fields=None):
    df = tide.solve_point_corr(lat, lon, alt, date, n=3600, increment='T')
    if fields is None:
        fields = ['g0']

    result = []
    for i, line in df.iterrows():
        data = {k: line[k] for k in fields}
        data['ts'] = line.name.timestamp()
        result.append(data)

    return result


def _tide_generator(lat, lon, alt):
    while True:
        ts = yield
        yield point_correction(lat, lon, alt, ts)


def get_tide_generator(lat, lon, alt):
    gen = _tide_generator(lat, lon, alt)
    gen.send(None)
    return gen


class ThreadedTideGenerator(threading.Thread):
    def __init__(self, lat, lon, alt, start_ts=None, publish_queue=None):
        super().__init__()
        self._exiting = threading.Event()
        self._sleep = 60
        self._queue = publish_queue or queue.Queue()
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self._start_time = start_ts or time.time()

    @property
    def queue(self):
        return self._queue

    def run(self):
        delta_ts = self._start_time - time.time()
        if delta_ts > 0:
            time.sleep(delta_ts)

        while not self._exiting.is_set():
            ts = datetime.now(tz=timezone.utc)
            gm, gs, g0 = point_correction(self.lat, self.lon, self.alt, date=ts)
            message = {'gm': gm, 'gs': gs, 'g0': g0, 'ts': ts}
            self._queue.put_nowait(message)
            time.sleep(self._sleep)



