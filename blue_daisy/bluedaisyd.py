#!/usr/bin/python3

import os

from daemonize import Daemonize

from config import Config
from server import BluetoothServer


PID_FILE = os.path.expanduser('~/.bluedaisy/bluedaisy.pid')


def run():
    while True:
        config = Config()
        server = BluetoothServer(config)
        server.receive_data()


if __name__ == '__main__':
    # create .bluedaisy directory if it does not exist
    os.makedirs(os.path.expanduser('~/.bluedaisy'), exist_ok=True)

    # create daemon
    daemon = Daemonize(app='BlueDaisy', pid=PID_FILE, action=run)
    daemon.start()
