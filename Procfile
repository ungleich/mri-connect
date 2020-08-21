web: gunicorn manage:app -b 0.0.0.0:$PORT -w 3 --log-file -
release: python manage.py deploy && yarn build
init: flask db upgrade
