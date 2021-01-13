## MRI Expert Database

An open source search engine and members directory for the [Mountain Research Initiative](https://mountainresearchinitiative.org/).

If you have any questions, please contact us via mri@mountainresearchinitiative.org

Currently under development by ungleich, [ungleich.ch](https://datalets.ch)

## Usage

To install, get a hold of **Python 3** and [Pipenv](https://github.com/pypa/pipenv) on your machine.

```bash
git clone https://gitlab.com/datalets/mri-connect.git
```

You also need to install the `postgis` and `gdal` to enable support for spatial computation.

You also need to enable `unaccent` extension for postgresql. You can do that by executing `psql -U app -c "CREATE EXTENSION \"unaccent\"";`

You can use `pip install -r requirements.txt`, but in development we use Poetry:

```bash
pip install -g poetry
poetry install
poetry shell
```

1. To create a blank database or upgrade the configured one:

    ```bash
    ./manage.py migrate
    ```

2. Create an admin account using:

    ```bash
    ./manage.py createsuperuser
    ```

3. Check for any new changes from the expert_management application
    ```bash
    ./manage.py makemigrations expert_management
    ```

4. To start the backend:
    ```bash
    ./manage.py runserver
    ```

## Data migration

To import data from the legacy database, use:
```bash
./manage.py importdata <xlsx_file_path>
```

## Load Mountains (GMBA)

To import mountains, use the following command
```bash
./manage.py loadgma <path_to_shp_file>
```

You can download the GMBA mountain registry from https://ilias.unibe.ch/goto_ilias3_unibe_file_1047348_download.html

## Deployment

`DJANGO_SETTINGS_MODULE="mriconnect.settings.prod"` in the environment ensures that production settings, loaded from the environment in `prod.py`, should be used.

Use a WSGI server like uwsgi to host the app in production mode.

Environment settings are set in the `app.ini`, e.g.:

```
env = DJANGO_SETTINGS_MODULE=mriconnect.settings.prod
env = ALLOWED_HOSTS=mri-staging.django-hosting.ch
env = LOG_DIR=/home/app/logs/
env = GOOGLE_MAP_API_KEY=google_map_api_key
env = EMAIL_HOST=smtp.example.com
env = EMAIL_PORT=587
env = EMAIL_HOST_USER=user@example.com
env = EMAIL_HOST_PASSWORD=password
env = DEFAULT_FROM_EMAIL=resetpassword@mri-staging.django-hosting.ch
```

Settings can also be provided using `mriconnect/settings/local.py`

## License

MIT - details in [LICENSE](LICENSE) file.
