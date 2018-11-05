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
        'folder': 'data',
        'filename': 'people_details',
        'required': ['ID', 'First name', 'Biography']
    },{
        'dataformat': DataFormat.RESOURCE_DETAIL,
        'extension': 'csv',
        'folder': 'data',
        'filename': 'resources',
        'required': ['ID', 'Citation', 'Abstract']
    },{
        'dataformat': DataFormat.RANGE_DETAIL,
        'extension': 'csv',
        'folder': 'data',
        'filename': 'ranges',
        'required': ['Range_ID', 'RangeName', 'GMBA_ID']
    },{
        'dataformat': DataFormat.PERSON_RESOURCE,
        'extension': 'csv',
        'folder': 'data',
        'filename': 'people_resources',
        'required': ['Resource', 'Person']
    },{
        'dataformat': DataFormat.PERSON_RANGE,
        'extension': 'csv',
        'folder': 'data',
        'filename': 'people_ranges',
        'required': ['ID', 'Person', 'MountainRange']
    },{
        'dataformat': DataFormat.RANGE_SHAPES,
        'extension': 'geojson',
        'folder': 'geodata',
        'filename': 'gmba',
        'required': ['Name', 'GMBA_ID']
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
