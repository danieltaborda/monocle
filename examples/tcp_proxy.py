import sys
import time

import monocle
from monocle import _o
monocle.init(sys.argv[1])

import socket

from monocle.stack import eventloop
from monocle.stack.network import add_service, Service, Client, ConnectionLost

@_o
def pump(input, output):
    while True:
        try:
            message = yield input.read_some()
            yield output.write(message)
        except ConnectionLost:
            output.close()
            break
        except socket.error:
            output.close()
            break

@_o
def handle_socks(conn):
    client = Client()
    yield client.connect('localhost', 8050)
    monocle.launch(pump, conn, client)
    yield pump(client, conn)

add_service(Service(handle_socks, port=7050))
eventloop.run()