## GMBA Connect

A search engine and members directory for the Global Mountain Biodiversity Assessment (GMBA) research network.

## Usage

Get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

    $ git clone https://gitlab.com/datalets/gmba-connect.git

To install and start the backend using Pipenv (Pip and Virtualenv should work fine too):

    $ pipenv --three
    $ pipenv install

To initialize and/or migrate the database:

    $ flask db init
    $ flask db migrate
    $ flask db upgrade

To start the backend:

    $ export FLASK_ENV="development"
    $ export FLASK_DEBUG=1
    $ python run.py

The interface will now be available at http://localhost:5000/admin

## Deployment

Use a WSGI server like Gunicorn to host the app in production mode, e.g.:

`gunicorn app:app`

The `Procfile` in this project folder makes it ready for deployment to Heroku.

## License

MIT - details in [LICENSE](LICENSE) file.
