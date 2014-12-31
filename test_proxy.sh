#!/bin/env python
# simple geven tcp proxy 
# client -> proxy -> echo
# client <- proxy <- echo

python gevent_echo.py &
python gevent_proxy.py &

python gevent_client.py
