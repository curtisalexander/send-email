#!/usr/bin/env bash

/path/to/script [parameters]
if [ $? -ne 0 ]; then
    send-email.py
fi
