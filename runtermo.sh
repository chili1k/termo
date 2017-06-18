#!/bin/bash

python /opt/termo/termo.py &
while true; do
  python /opt/termo/termoread.py
  # Read data every 5 minutes
  sleep 300
done
