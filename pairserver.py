# For learning
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pair.html
import json
import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

while True:
    msg = socket.recv()
    if msg:
        decoded_msg = json.loads(msg.decode())
        print('received', decoded_msg)
        numbers = decoded_msg["numbers"]
        to_send = json.dumps({"sum": sum(numbers)}).encode()
        socket.send(to_send)
        print('sent', to_send)
    time.sleep(1)
