# -*- coding: utf-8 -*-
"""
bluedaisy.server
~~~~~~~~~~~~~~~~

This module provides the capability to establish a bluetooth connection
with a client device.
"""

import json

import bluetooth as bt


class BluetoothServer:
    """Establish and maintain a bluetooth connection.

    Attributes:
        _server_socket (bluetooth.BluetoothSocket): A server socket.

        _client_socket (bluetooth.BluetoothSocket): A client socket.

        config (bluedaisy.config.Config): Handles the commands received from
            the client device.
    """

    _server_socket = None
    _client_socket = None

    def __init__(self, config):
        """BluetoothServer class constructor.

        Args:
            config (bluedaisy.config.Config): An instance of
                ``bluedaisy.config.Config`` to handle commands received from
                the client device.
        """
        self.config = config
        self._init_sockets()

    def receive_data(self):
        """Receive data from the client once a connection is established."""
        try:
            while True:
                data = self._client_socket.recv(1024).decode('utf-8')
                if len(data) == 0:
                    continue

                try:
                    # convert the json to python dictionary
                    command = json.loads(data)
                except json.decoder.JSONDecodeError:
                    continue

                if isinstance(command, dict):
                    section = command.get('section', None)
                    option = command.get('option', None)

                    self.config.execute_command(section, option)

        except IOError:
            pass

        self._close()

    def _init_sockets(self):
        """Initialize server and client sockets."""
        if not self._server_socket and not self._client_socket:
            self._server_socket = bt.BluetoothSocket(bt.RFCOMM)
            self._server_socket.bind(('', bt.PORT_ANY))
            self._server_socket.listen(1)

            uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee'

            bt.advertise_service(
                self._server_socket, 'BlueDaisyServer',
                service_id=uuid,
                service_classes=[uuid, bt.SERIAL_PORT_CLASS],
                profiles=[bt.SERIAL_PORT_PROFILE]
            )

            # establish connection with client
            self._client_socket = self._server_socket.accept()[0]

    def _close(self):
        """Close the server and client sockets."""
        if self._client_socket:
            self._client_socket.close()

        if self._server_socket:
            self._server_socket.close()
