import gevent
from gevent import socket

def connect_client():
    client = socket.create_connection(('127.0.0.1', 1234), 0.001)
    client.send("hello, word.\r\n")
    gevent.socket.wait_read(client.fileno())
    print "send ok."
    data = client.recv(20)
    print "recv: %r" % (data)


jobs = []
for i in xrange(1000):
    jobs.append(gevent.spawn(connect_client))

gevent.joinall(jobs, timeout=20)
