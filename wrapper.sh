#!/usr/bin/env bash

/path/to/script [parameters]
# http://tldp.org/LDP/abs/html/exit-status.html
# $? ==> reads the exit status of the last command executed
# $? -eq 0 is success
# $? -ne 0 is failure
if [ $? -ne 0 ]; then
    send-email.py --config failure.yaml
else
    send-email.py --config success.yaml
fi
