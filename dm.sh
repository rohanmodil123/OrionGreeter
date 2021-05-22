#!/usr/bin/env bash

/usr/bin/Xephyr :2 &
DISPLAY=:2 /root/OrionGreeter/gui.sh
