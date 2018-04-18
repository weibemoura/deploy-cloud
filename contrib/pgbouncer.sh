#!/usr/bin/env bash

source activate deploy > /dev/null
pip install -r requirements.txt > /dev/null
fab -f main pgbouncer