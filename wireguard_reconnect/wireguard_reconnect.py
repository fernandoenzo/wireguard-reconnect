#!/usr/bin/env python3
# encoding:utf-8

import os
import signal
import sys
from threading import Event

from wireguard_reconnect.parser import parse_args, ARGS
from wireguard_reconnect.utils import print_flush as print, run_command, header

loop = True
sleep_event = Event()


def close(signum, frame):
    global loop
    loop = False
    sleep_event.set()
    print('Stop signal received')


signal.signal(signal.SIGTERM, close)
signal.signal(signal.SIGINT, close)


def link_up():
    ret = run_command(['ip', 'link', 'show', ARGS.INTERFACE], systemd=ARGS.SYSTEMD)
    return not ret.returncode


def ping():
    if ARGS.GATEWAY is None:
        return True
    ret = run_command(['ping', '-W5', '-c3', '-I', ARGS.INTERFACE, ARGS.GATEWAY], systemd=ARGS.SYSTEMD)
    return not ret.returncode


def set_wg():
    ret = run_command(['wg-quick', 'up', ARGS.INTERFACE], systemd=ARGS.SYSTEMD)
    if ret.stderr.count('does not exist'):
        print(ret.stderr, end='')
        sys.exit(1)
    if ret.returncode == 0:
        if link_up() and ping():
            return True
        unset_wg()
    return False


def unset_wg():
    ret = run_command(['wg-quick', 'down', ARGS.INTERFACE], systemd=ARGS.SYSTEMD)
    return not ret.returncode


def reconnect():
    up_message = f"WireGuard interface '{ARGS.INTERFACE}' is currently UP"
    down_message = f"WireGuard interface '{ARGS.INTERFACE}' is currently DOWN"
    if link_up():
        if ping():
            print(up_message)
        else:
            unset_wg()
            print(down_message)
    else:
        print(up_message) if set_wg() else print(down_message)


def main():
    if os.getuid() != 0:
        print('This program must be run with root privileges.')
        sys.exit(0)
    print(header('WireGuard Reconnect'))
    parse_args()
    ARGS.SYSTEMD = not run_command(['pidof', 'systemd'], systemd=False).returncode
    print(f'Interface: {ARGS.INTERFACE}\nGateway: {ARGS.GATEWAY}\nRecheck period: {ARGS.PERIOD}s\n ')
    while loop:
        reconnect()
        sleep_event.wait(ARGS.PERIOD)
    unset_wg()
    print(f"Disabled WireGuard interface '{ARGS.INTERFACE}'")
