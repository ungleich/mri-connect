#!/usr/bin/env bash

cwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${cwd}

export FLASK_CONFIG="Production"
python ./run.py
