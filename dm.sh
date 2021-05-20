#!/usr/bin/env bash

/usr/bin/Xephyr :2 &
DISPLAY=:2 /mnt/hdd/rcode/OrionLDMG/dm.py
