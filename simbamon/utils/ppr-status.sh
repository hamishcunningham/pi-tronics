#!/bin/bash

[ -z "$1" ] && { echo usage: $0 status-word; exit 1; }
echo 0123456789012345
echo "obase=2;$1;" |bc |rev
