## MRI Connect

An open source search engine and members directory for the [Mountain Research Initiative](https://mountainresearchinitiative.org/).

Currently under development.

If you have any questions, please contact us via (info@) [datalets.ch](https://datalets.ch)

## Usage

This project is based on the [Django] and Vue.js web application platforms.

To install, get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

    $ git clone https://gitlab.com/datalets/mri-connect.git

You can use `pip install -r requirements.txt`, but in development we use Poetry:

    $ pip install -g poetry
    $ poetry install
    $ poetry shell

1. To create a blank database or upgrade the configured one:

    $ ./manage.py migrate

2. Create an admin account using:

    $ ./manage.py createsuperuser

3. Check for any new changes from the People application

    $ ./manage.py makemigrations people

4. To start the backend:

    $ ./manage.py runserver

5. To build the frontend, install nodejs npm and [yarn](https://yarnpkg.com/), then:

    $ yarn

The frontend interface will be available in `dist`. Use `yarn serve` in development for live reloading.

Check the log for the port and URL to the admin interface.

## Data migration

To import data from the legacy database (`filename` = CSV export), use:

    $ ./manage.py mriload <filename>

Check the `convert` folder for supplementary conversion datafiles.

## Deployment

Use a WSGI server like uwsgi to host the app in production mode.

To save changes from the poetry environment to `requirements.txt`:

    poetry export -f requirements.txt > requirements.txt

## License

MIT - details in [LICENSE](LICENSE) file.
