"""
In this example, we use a RunEngine in the normal fashion while also
calling it from a background thread that is listening for commands from
a 0MQ PAIR.

To enable this, we have to disable some of the RunEngine's features related
to dealing with Qt (in particular matploblib with a Qt backend) and threading
and interrupt (SIGINT) handling. Disabling these features enables us to call
RE(...) from the background thread that is listening to 0MQ.

There are certainly better ways to do this, but this is one quick way.
"""
import asyncio
import contextlib
import json
import zmq
import random
import sys
import time
import threading

from bluesky.plans import scan
from ophyd.sim import det, motor
from bluesky import RunEngine
from bluesky.utils import DuringTask


RE = RunEngine(during_task=DuringTask(), context_managers=[])


def serve():
    log = lambda *msg: print(*msg, flush=True)
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)

    while True:
        log('listening')
        msg = socket.recv()
        print('received')
        if msg:
            try:
                log('received request from 0MQ:', msg)
                decoded_msg = json.loads(msg.decode())
                plan = eval(decoded_msg["plan_name"], globals())
                plan_args = eval(decoded_msg["plan_args"], globals())
                plan_kwargs = eval(decoded_msg["plan_kwargs"], globals())
                log('running plan')
                result = RE(plan(*plan_args, **plan_kwargs))
                log('plan complete')
                to_send = json.dumps({"result": result}).encode()
                print('sending', to_send)
                socket.send(to_send)
                log('sent', to_send)
            except Exception:
                log(f"Failed to process {msg}")

thread = threading.Thread(target=serve, daemon=True)
thread.start()
