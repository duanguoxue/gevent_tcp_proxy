#!/usr/bin/env python

import gevent
from gevent import socket
from gevent.server import StreamServer
import signal
import os

def handle_echo(sock, address):
    fp = sock.makefile()
    while True:
        line = fp.readline()
        if line:
            print(os.getpid()) 
            fp.write(line)
            fp.flush()
        else:
            break
    sock.shutdown(socket.SHUT_WR)
    sock.close()

# create server socket
sock = socket.socket()
sock.bind(('', 1235))
sock.listen(256)

# bind server socket to gevent
server = StreamServer(sock, handle_echo)

def serve_for_ever(): 
    global server
    server.start_accepting()
    server.serve_forever()

def server_stop():
    global server
    print("stop")
    server.stop()

gevent.signal(signal.SIGINT, server_stop)
serve_for_ever()

