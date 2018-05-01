# -*- coding: utf-8 -*-

import argparse

from .sqs_supplier import SQSSupplier


def parse_args():
    parser = argparse.ArgumentParser(description='Tide SQS Daemon')
    parser.add_argument('--lat', action='store', type=float, required=True)
    parser.add_argument('--lon', action='store', type=float, required=True)
    parser.add_argument('--alt', action='store', type=float, required=True)
    parser.add_argument('--queue', action='store', type=str, required=True)
    parser.add_argument('--delay', action='store', type=int, default=60)
    parser.add_argument('--aws-profile', action='store', type=str, default='default')

    return parser.parse_args()


def main():
    """CLI entry-point"""
    opts = parse_args()
    supplier = SQSSupplier(opts.lat, opts.lon, opts.alt, opts.queue, delay=opts.delay, aws_profile=opts.aws_profile)
    supplier.start()


main()
