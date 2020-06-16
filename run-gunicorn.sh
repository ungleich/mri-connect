#!/usr/bin/env bash

export FLASK_ENV="development"
export FLASK_DEBUG=1

gunicorn app:app
