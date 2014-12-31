#!/usr/bin/env python

import gevent
from gevent import socket
from gevent.server import StreamServer
import signal
import os
count = 0

def get_client():
    return socket.create_connection(("127.0.0.1", 1235), 0.001)

def send_and_recv(sock, data):
    sock.send(data)
    print('send:', data)
    gevent.socket.wait_read(sock.fileno())
    recv_data = sock.recv(1024)
    print('recv:', recv_data)
    return recv_data

def handle_echo(sock, address):
    global count
    fp = sock.makefile()
    client = get_client()
    while True:
        line = fp.readline()
        if line:
            count = count +1
            print(count, os.getpid())
            task = gevent.spawn(send_and_recv, client, line)
            task.join()
            print "recv", task.value
            fp.write(task.value)
            fp.flush()
        else:
            break
    #sock.shutdown(socket.SHUT_WR)
    client.close()
    sock.close()

# create server socket
sock = socket.socket()
sock.bind(('', 1234))
sock.listen(256)

# bind server socket to gevent
server = StreamServer(sock, handle_echo)

def serve_for_ever(): 
    global server
    server.start_accepting()
    server.serve_forever()

def server_stop():
    global server
    print("SIGINT safe stop")
    server.stop()

#from multiprocessing import Process
# multi process 
"""process_count = 2 
for i in range(process_count - 1):
    Process(target=serve_for_ever, args=tuple()).start()
"""
gevent.signal(signal.SIGINT, server_stop)
serve_for_ever()

