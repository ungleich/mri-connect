#!/usr/bin/env bash

cwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${cwd}

export FLASK_ENV="development"
export FLASK_DEBUG=1
python ./run.py
