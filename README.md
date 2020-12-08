## MRI Connect

An open source search engine and members directory for the [Mountain Research Initiative](https://mountainresearchinitiative.org/).

If you have any questions, please contact us via mri@mountainresearchinitiative.org

Currently under development by Oleg Lavrovsky, [datalets.ch](https://datalets.ch)

## Usage

This project is based on the [Django] and Vue.js web application platforms.

To install, get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

    $ git clone https://gitlab.com/datalets/mri-connect.git

You also need to install the `libspatialite` (or `postgis` for production) and `gdal` to enable support for spatial computation.

You can use `pip install -r requirements.txt`, but in development we use Poetry:

    $ pip install -g poetry
    $ poetry install
    $ poetry shell

1. To create a blank database or upgrade the configured one:

    $ ./manage.py migrate

2. Create an admin account using:

    $ ./manage.py createsuperuser

3. Check for any new changes from the expert_management application

    $ ./manage.py makemigrations expert_management

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

`DJANGO_SETTINGS_MODULE="mriconnect.settings.prod"` in the environment ensures that production settings, loaded from the environment in `prod.py`, should be used.

Use a WSGI server like uwsgi to host the app in production mode. Environment settings are set in the `app.ini`, e.g.:

```
env = DJANGO_SETTINGS_MODULE=mriconnect.settings.prod
env = ALLOWED_HOSTS=mri.django-hosting.ch
env = LOG_DIR=/home/app/logs/
```

Settings can also be provided using `mriconnect/settings/local.py`

## Releases

To save dependency changes from the poetry environment to `requirements.txt`:

    poetry export -f requirements.txt > requirements.txt

## License

MIT - details in [LICENSE](LICENSE) file.
