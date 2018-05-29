# -*- coding: utf-8 -*-

import argparse
import logging
import time
import sys
from datetime import datetime, timedelta
from queue import Queue

from .TideGenerator import get_tide_generator
from .SQSPublisher import SQSPublisher


def parse_args():
    parser = argparse.ArgumentParser(description='Tide SQS Daemon')
    parser.add_argument('--lat', action='store', type=float, required=True)
    parser.add_argument('--lon', action='store', type=float, required=True)
    parser.add_argument('--alt', action='store', type=float, required=True)
    parser.add_argument('--queue', action='store', type=str, required=True)
    parser.add_argument('--batch', action='store_true')
    parser.add_argument('--purge', action='store_true')
    parser.add_argument('--delay', action='store', type=int)
    parser.add_argument('--generate', action='store', type=int)
    parser.add_argument('--aws-profile', action='store', type=str, default='default')
    parser.add_argument('--aws-region', action='store', type=str, default='us-west-2')

    return parser.parse_args()


def main():
    """CLI entry-point"""
    logging.basicConfig(format="%(asctime)s - %(levelName)s - %(message)s")
    log = logging.getLogger()
    opts = parse_args()

    sqs = SQSPublisher(opts.queue, opts.aws_profile, opts.aws_region)
    try:
        sqs.connect()
    except ConnectionError:
        log.exception("Exception establishing connection to SQS endpoint.")

    msg_queue = Queue()
    tide_gen = get_tide_generator(opts.lat, opts.lon, opts.alt)
    while True:
        ts = datetime.now()
        gm, gs, g0 = tide_gen.send(ts)
        msg_queue.put_nowait(dict(g0=g0, ts=ts))
        time.sleep(opts.delay)







main()
