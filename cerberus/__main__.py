#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import asyncio
from cerberus.const import *
from cerberus.tcs import TCSBusReader, TCSBusWriter, wiringPiSetupGpio
from cerberus.worker import TCSTunnelWorker, WSWorker, TCSBusWorker, UARTWorker, HomeAssistantWorker
import argparse
import yaml

def parse_arguments() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(
        description=__doc__)

    argparser.add_argument(
        '-l', '--listen',
        metavar='L',
        default=WS_IP,
        help='IP of the WebSocket server to listen on (default: %s)' % (WS_IP))
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=WS_PORT,
        type=int,
        help='TCP port to listen to (default: %i)' % (WS_PORT))
    argparser.add_argument(
        '-i', '--interrupt-pin',
        metavar='I',
        default=INTERRUPT_PIN,
        type=int,
        help='Pin number where to write the interrupt to (default: %i)' % (INTERRUPT_PIN))
    argparser.add_argument(
        '-r', '--read-pin',
        metavar='R',
        default=READ_PIN,
        type=int,
        help='TCS read pin number (default: %i)' % (READ_PIN))
    argparser.add_argument(
        '-w', '--write-pin',
        metavar='W',
        default=WRITE_PIN,
        type=int,
        help='TCS write pin number (default: %i)' % (WRITE_PIN))

    return argparser.parse_args()

def main(args=None):
    with open('config.yaml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            print('config.yaml loaded')
        except yaml.YAMLError as exc:
            config = {}
            print('config.yaml not loaded')

    args = parse_arguments()
    GPIO.setmode(GPIO.BCM)
    wiringPiSetupGpio()

    use_uart = False

    tcs_bus_worker = TCSBusWorker(TCSBusReader(args.read_pin), TCSBusWriter(args.write_pin))

    uart_worker = UARTWorker()
    tcs_tunnel_worker = TCSTunnelWorker(args.interrupt_pin)

    ws_worker = WSWorker(uart_worker if use_uart else tcs_bus_worker, ip=args.listen, port=args.port)
    home_assistant_worker = HomeAssistantWorker(
        uart_worker if use_uart else tcs_bus_worker,
        config['home_assistant']['url'],
        config['home_assistant']['api_token'],
        config['home_assistant']['google_home_entity_id'],
        config['home_assistant']['media']
    ) if 'home_assistant' in config else None

    def exit_signal_handler(sig, frame):
        if not use_uart:
            tcs_tunnel_worker.stop()

        (uart_worker if use_uart else tcs_bus_worker).stop()

        ws_worker.stop()

        GPIO.cleanup()

        sys.exit(0)

    signal.signal(signal.SIGINT, exit_signal_handler)

    if not use_uart:
        print('Starting TCS Tunnel Worker')
        tcs_tunnel_worker.start()

    print('Starting Websocket Worker')
    ws_worker.start()

    print('Starting %s' % ((uart_worker if use_uart else tcs_bus_worker).name))
    (uart_worker if use_uart else tcs_bus_worker).start()

    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    sys.exit(main())