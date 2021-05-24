#!/usr/bin/env bash

/usr/bin/Xephyr :2 &
DISPLAY=:2 /home/rohan/OrionGreeter/gui.sh
