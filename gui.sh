#!/usr/bin/env bash

/usr/bin/X :0 &
DISPLAY=:0 /home/rohan/OrionGreeter/dm.py
