## MRI Connect

A search engine and members directory for the Mountain Research Initiative.

(Work in progress)

## Usage

Get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

    $ git clone https://gitlab.com/datalets/mri-connect.git

To install and start the backend using Poetry:

    $ pip install -g poetry
    $ poetry install
    $ poetry shell

To create a blank database or upgrade the configured one:

    $ flask db upgrade

To initialize and/or migrate the database, if necessary:

    $ flask db init
    $ flask db migrate

To start the backend:

    $ export FLASK_ENV="development"
    $ export FLASK_DEBUG=1
    $ python run.py

To build the frontend:

    $ yarn

The frontend interface will now be available.

Check the log for the port and URL to the admin interface.

## Deployment

Use a WSGI server like Gunicorn to host the app in production mode, e.g.:

`gunicorn app:app`

The `Procfile` in this project folder makes it ready for deployment to Heroku.

## License

MIT - details in [LICENSE](LICENSE) file.
