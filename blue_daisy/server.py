import json

import bluetooth as bt

from .config import Config


class BluetoothServer:

    _server_socket = None
    _client_socket = None

    def __init__(self):
        self._init_sockets()

    def receive_data(self):
        try:
            while True:
                data = self._client_socket.recv(1024)
                if len(data) == 0:
                    break

                command = json.loads(data)
                if isinstance(command, dict):
                    section = command.get('section', None)
                    option = command.get('option', None)

                    config = Config()
                    config.execute_command(section, option)

        except IOError:
            pass

        self._close()

    def _init_sockets(self):
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

            self._client_socket = self._server_socket.accept()[0]

    def _close(self):
        if self._client_socket:
            self._client_socket.close()

        if self._server_socket:
            self._server_socket.close()
