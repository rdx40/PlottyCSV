#!/bin/bash
until flask run --host=0.0.0.0 --port=5000; do
    echo "Flask crashed with exit code $?. Respawning..." >&2
    sleep 1
done

