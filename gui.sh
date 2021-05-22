#!/usr/bin/env bash

/usr/bin/X :0 &
DISPLAY=:0 /root/OrionGreeter/dm.py
