#!/usr/bin/python
import argparse
import sys
import signal
import time
import logging
from log import log


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Simple Hello World Demo')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', required=False, default=False,
                        help='Enable debug messages')
    return parser.parse_args()

def main():
    # Catch all Control+C's
    def handler(signum, frame):
        log('Signal handler called with signal {}'.format(signum), 10)
        sys.exit(0)

    # Register the handler for Ctl+C
    signal.signal(signal.SIGINT, handler)

    args = parse_args(sys.argv)
    logger = logging.getLogger(__name__)
    if args.verbose:
        logger.setLevel(10)
    else:
        logger.setLevel(20)

    time.sleep(.2)
    print 'Hello World!'

if __name__ == '__main__':
    main()
