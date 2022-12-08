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


def run(plan_name, args, kwargs):
    to_send = json.dumps({"plan_name": plan_name, "plan_args": args, "plan_kwargs": kwargs}).encode()
    socket.send(to_send)
    print('sent', to_send)
    msg = socket.recv()
    if msg:
        decoded_msg = json.loads(msg.decode())
        print('received', decoded_msg)


if __name__ == "__main__":
    run("scan", "([det], motor, 1, 5, 5)", "{}")
