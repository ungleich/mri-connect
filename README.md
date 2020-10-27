## MRI Connect

A search engine and members directory for the Mountain Research Initiative.

[This diagram](dataflow.png) contains an overview of the architecture of the project.

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

There is a convenience script (`deploy`) with the above functions as well as profiling (`profile`) and testing (`test`) routines, e.g.:

    $ python manage.py deploy

To start the backend:

    $ export FLASK_ENV="development"
    $ export FLASK_DEBUG=1
    $ flask run

To build the frontend:

    $ yarn

The frontend interface will now be available. Use `yarn serve` in development.

Check the log for the port and URL to the admin interface.

## Deployment

Use a WSGI server like Gunicorn to host the app in production mode, e.g.:

`gunicorn app:app`

The `Procfile` in this project folder makes it ready for deployment to Heroku.

Note that you need to save changes to the poetry environment to `requirements.txt`:

    poetry export -f requirements.txt > requirements.txt

## License

MIT - details in [LICENSE](LICENSE) file.
