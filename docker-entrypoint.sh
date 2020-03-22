#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/resume_valuation
nohup redis-server &
python ./app.py
