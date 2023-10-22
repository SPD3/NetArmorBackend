#!/bin/sh

while true; do
    python -m src.main &
    PID=$!
    inotifywait -q src/*.py
    kill $PID
done