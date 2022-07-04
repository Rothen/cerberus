#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import asyncio
from cerberus.api import api_token_container
from cerberus.const import *
from cerberus.tcs import TCSBusReader, TCSBusWriter, wiringPiSetupGpio
from cerberus.worker import TCSTunnelWorker, WSWorker, TCSBusWorker, UARTWorker
from cerberus.api import APITokenContainer
import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__)

    main_group = parser.add_mutually_exclusive_group(required=True)
    add_remove_name_group = main_group.add_argument_group()

    main_group.add_argument(
        '-l', '--list',
        action='store_true',
        help='Lists all API Tokens')

    main_group.add_argument(
        '-a', '--add',
        action='store_true',
        help='Adding an API Token')

    main_group.add_argument(
        '-r', '--remove',
        action='store_true',
        help='Remove an API Token')

    add_remove_name_group.add_argument(
        '-n', '--name',
        metavar='N',
        help='Name of the API Token')

    args = parser.parse_args()
    
    if (args.add or args.remove) and args.name is None:
        parser.error("--name required with --add or --remove")

    return args

def main() -> None:
    args = parse_arguments()

    api_token_container = APITokenContainer()

    if args.add:
        api_token_container.generate(args.name)
    elif args.remove:
        api_token_container.remove(args.name)
    elif args.list:
        api_token_container.list()


if __name__ == '__main__':
    sys.exit(main())