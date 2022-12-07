# For learning
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pair.html
import itertools
import json
import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

for i in itertools.count(0):
    to_send = json.dumps({"numbers": [i, 1+i]}).encode()
    socket.send(to_send)
    print('sent', to_send)
    msg = socket.recv()
    if msg:
        decoded_msg = json.loads(msg.decode())
        print('received', decoded_msg)
    time.sleep(1)
