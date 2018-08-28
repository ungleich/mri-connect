from enum import Enum

class DataFormat(Enum):
    PERSON_DETAIL = 1
    PERSON_RESOURCE = 2
    PERSON_RANGE = 3
    RESOURCE_DETAIL = 4
    RANGE_SHAPES = 5
    RANGE_DETAIL = 6

DATAFORMATS = [
    {
        'dataformat': DataFormat.PERSON_DETAIL,
        'extension': 'csv',
        'filename': 'people_details',
        'required': ['ID', 'First name', 'Biography']
    },{
        'dataformat': DataFormat.RESOURCE_DETAIL,
        'extension': 'csv',
        'filename': 'resources',
        'required': ['ID', 'Citation', 'Abstract']
    },{
        'dataformat': DataFormat.RANGE_DETAIL,
        'extension': 'csv',
        'filename': 'ranges',
        'required': ['Range_ID', 'RangeName', 'GMBA_ID']
    },{
        'dataformat': DataFormat.RANGE_SHAPES,
        'extension': 'geojson',
        'filename': 'gmba',
        'required': ['Name', 'GMBA_ID']
    },{
        'dataformat': DataFormat.PERSON_RESOURCE,
        'extension': 'csv',
        'filename': 'people_resources',
        'required': ['Resource', 'Person']
    },{
        'dataformat': DataFormat.PERSON_RANGE,
        'extension': 'csv',
        'filename': 'people_ranges',
        'required': ['ID', 'Person', 'MountainRange']
    }
]

def detect_dataformat(row):
    if row is None: return None
    for fmt in DATAFORMATS:
        missing_property = False
        for prop in fmt['required']:
            if not prop in row: missing_property = True
        if not missing_property:
            return fmt
    return None
