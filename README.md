## MRI Expert Database

An open source search engine and members directory for the [Mountain Research Initiative](https://mountainresearchinitiative.org/).

If you have any questions, please contact us via mri@mountainresearchinitiative.org

Currently under development by ungleich, [ungleich.ch](https://datalets.ch)

## Usage

To install, get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

    $ git clone https://gitlab.com/datalets/mri-connect.git

You also need to install the `postgis` and `gdal` to enable support for spatial computation.

You also need to enable `unaccent` extension for postgresql. You can do that by executing `psql -U app -c "CREATE EXTENSION \"unaccent\"";`

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


## Data migration

To import data from the legacy database, use:

    $ ./manage.py importdata <filepath>

## Deployment

`DJANGO_SETTINGS_MODULE="mriconnect.settings.prod"` in the environment ensures that production settings, loaded from the environment in `prod.py`, should be used.

Use a WSGI server like uwsgi to host the app in production mode. Environment settings are set in the `app.ini`, e.g.:

```
env = DJANGO_SETTINGS_MODULE=mriconnect.settings.prod
env = ALLOWED_HOSTS=mri.django-hosting.ch
env = LOG_DIR=/home/app/logs/
```

Settings can also be provided using `mriconnect/settings/local.py`

## License

MIT - details in [LICENSE](LICENSE) file.
