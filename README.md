# RE + 0MQ Experiments

This is a temporary scratch project for understanding possible Bluesky
RunEninge <---> 0MQ interactions.

```
$ pip install bluesky ophyd pyzmq ipython
```

```
$ ipython -i server.py
Python 3.9.13 (main, Oct 13 2022, 21:15:33)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

listening
In [1]: RE(scan([det], motor, 1, 3, 3))  # normal direct usage
Out[1]: ('6451290b-d081-4998-bbee-04dbb131441b',)

# processing a request received over 0MQ from the client --- see below
received
received request from 0MQ: b'{"plan_name": "scan", "plan_args": "([det], motor, 1, 5, 5)", "plan_kwargs": "{}"}'
running plan
plan complete
sending b'{"result": ["03adc7de-a6ac-4343-94bf-21a440a2823c"]}'
sent b'{"result": ["03adc7de-a6ac-4343-94bf-21a440a2823c"]}'
listening
```

```
$ python client.py
sent b'{"plan_name": "scan", "plan_args": "([det], motor, 1, 5, 5)", "plan_kwargs": "{}"}'
received {'result': ['03adc7de-a6ac-4343-94bf-21a440a2823c']}
```
