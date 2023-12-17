#!/bin/bash

cd /data/zbw/MIG/MIG/ATC-MIG

python main.py --type worker & python main.py --type scheduler
