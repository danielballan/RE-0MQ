import json
import zmq
import random
import sys
import time
import threading

from bluesky.plans import scan
from ophyd.sim import det, motor
from bluesky import RunEngine


class REProxy:
    def __init__(self, RE):
        self.RE = RE

    def __getattr__(self, key):
        return self.RE

    def __call__(self, *args, **kwargs):
        try:
            return self.RE(*args, **kwargs)
        except Exception:
            if self.RE.state == "running":
                raise RuntimeError("RE is busy running remote plan")
            raise


internal_RE = RunEngine()
RE = REProxy(internal_RE)
print(RE(scan([det], motor, 1, 5, 5)))

def serve():
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)

    while True:
        msg = socket.recv()
        if msg:
            decoded_msg = json.loads(msg.decode())
            plan = eval(decoded_msg["plan_name"], globals())
            plan_args = eval(decoded_msg["plan_args"], globals())
            plan_kwargs = eval(decoded_msg["plan_kwargs"], globals())
            result = internal_RE(plan(*plan_args, **plan_kwargs))
            to_send = json.dumps({"result": result}).encode()
            socket.send(to_send)
            print('sent', to_send)

thread = threading.Thread(target=serve, daemon=True)
thread.start()
