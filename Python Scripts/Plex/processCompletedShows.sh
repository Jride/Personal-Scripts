#!/bin/bash

source ~/.bash_profile

python3 "$PYTHON_SCRIPTS/Plex/ProcessCompletedTorrents.py" -mediaTypesdf show
