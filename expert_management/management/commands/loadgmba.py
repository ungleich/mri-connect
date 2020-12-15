from pathlib import Path

from django.contrib.gis.utils import LayerMapping
from django.core.management import BaseCommand, CommandError

from expert_management.models import Mountain


class Command(BaseCommand):
    help_text = "Import .shp files into Mountain model"

    def add_arguments(self, parser):
        parser.add_argument("path_to_shp")

    def handle(self, *args, **options):
        path_to_shp = Path(options["path_to_shp"]).resolve()
        mapping = {
            "name": "Name",
            "country": "Country",
            "mpoly": "POLYGON"
        }
        lm = LayerMapping(Mountain, str(path_to_shp), mapping, encoding="latin-1")
        lm.save(verbose=True)
