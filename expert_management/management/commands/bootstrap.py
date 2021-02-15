from django.core.management import BaseCommand

from expert_management import models


MOUNTAIN_NAMES = [
    'Alps', 'Andes', 'Appalachian Mountains', 'Atlas', 'Balkan', 'Cape Ranges', 'Carpathians', 'Caucasus',
    'Drakensberg', 'Eastern Arc Mountains', 'Ethiopian Highlands', 'Great Dividing Range', 'Himalaya',
    'Japanese Alps', 'Kalahari', 'Kamchatka Range', 'Karelides', 'Pyrenees', 'Rocky Mountains',
    'Scottish Highlands', 'Siberian Plateau', 'Sierra Madre', 'Southern Alps New Zealand'
]
RESEARCH_EXPERTISE_SUB_CATEGORIES = [
    'Basic Research', 'Applied Research', 'Research Interface and Management', 'Interdisciplinary Research',
    'Transdisciplinary Research'
]

ATMOSPHERIC_SCIENCES_SUB_CATEGORIES = ['Meteorology', 'Climatology', 'Atmospheric Physics / Chemistry', 'Pollution']

HYDROSPERIC_SCIENCES_SUB_CATEGORIES = ['Fresh Water Systems', 'Precipitation and Runoff', 'Hydrogeology']

CRYOSPHERIC_SCIENCES_SUB_CATEGORIES = ['Glaciology', 'Snow Sciences', 'Permafrost and solifluction']

EARTH_SCIENCES_SUB_CATEGORIES = [
    'Soil Science/Pedology', 'Geomorphology', 'Geochemistry', 'Geology', 'Physical Geography', 'Geophysics'
]

BIOLOGICAL_SCIENCES_SUB_CATEGORIES = [
    'Botany', 'Zoology', 'Ecology', 'Terrestrial Ecosystems', 'Aquatic Ecosystems', 'Soil organisms',
    'Forestry', 'Ecosystem functioning', 'Ecosystem services', 'Biodiversity'
]

SOCIAL_SCIENCES_AND_HUMANITIES_SUB_CATEGORIES = [
    'History, classical studies, archaeology, prehistory and early history', 'Linguistics and literature, philosophy',
    'Art studies, musicology, theatre and film studies, architecture', 'Ethnology, social and human geography',
    'Psychology', 'Educational studies', 'Sociology, social work', 'Political sciences',
    'Media and communication studies', 'Public health', 'Economics', 'Law'
]

INTEGRATED_SYSTEMS_SUB_CATEGORIES = [
    'Carbon Cycle', 'Other Biogeochemical Cycles', 'Hydrogeochemical Cycle', 'Nutrient Cycle',
    'Social-ecological Systems'
]

SPATIAL_SCALE_OF_EXPERTISE_SUB_CATEGORIES = [
    'Global / Hemispheric', 'Continental', 'Regional', 'National / Cultural', 'Local / Community', 'Other'
]

STATISTICAL_FOCUS_SUB_CATEGORIES = ['Extremes', 'Mean Change / Trends', 'Variability', 'Other']

TIME_SCALES_SUB_CATEGORIES = [
    'Seasonal / Annual', 'Decadal / Centennial', 'Millenial', '100 kyr', 'Billenial (Mio yrs)', 'Other'
]

METHODS_SUB_CATEGORIES = [
    'Earth Observations', 'Remote sensing', 'Field observations', 'Field Experiments', 'Modeling',
    'Spatial analysis', 'Policy Analysis', 'Qualitative social science methods', 'Integrative assessments',
    'Synthesis and meta-analysis', 'Other'
]

PARTICIPATION_IN_ASSESSMENTS_SUB_CATEGORIES = ['IPCC', 'IPBES', 'UNDRR GAR']

INPUTS_OR_PARTICIPATION_TO_UN_CONVENTIONS_SUB_CATEGORIES = [
    'UN Agenda 2030 (SDGs) / UN HLPF', 'UNFCCC', 'CBD', 'UNDRR Sedai', 'UNCCD'
]

SWISS_CHEESE = [
    'Sbrinz', 'Berner Hobelkäse', 'Appenzeller', 'Berner Alpkäse', 'Bündner Bergkäse',
    'Gruyère/Greyerzer', "L'Etivaz", 'Röthenbacher Bergkäse', 'Mutschli', 'Schabziger',
    'Tête de Moine', 'Emmentaler', 'Raclette', 'Scharfe Maxx', 'Le Marechal', 'Tilsiter',
    'Vacherin Fribourgeois', 'Formaggini', 'Luzerner Rahmkäse', "Vacherin Mont d'Or",
    'Gala', 'Büsciun da cavra', 'Tomme Vaudoise', 'Bleuchâtel'
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Mountain.objects.bulk_create(
            [models.Mountain(name=name) for name in MOUNTAIN_NAMES], ignore_conflicts=True
        )
        models.ResearchExpertise.objects.bulk_create(
            [models.ResearchExpertise(title=title) for title in RESEARCH_EXPERTISE_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.AtmosphericSciences.objects.bulk_create(
            [models.AtmosphericSciences(title=title) for title in ATMOSPHERIC_SCIENCES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.HydrosphericSciences.objects.bulk_create(
            [models.HydrosphericSciences(title=title) for title in HYDROSPERIC_SCIENCES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.CryosphericSciences.objects.bulk_create(
            [models.CryosphericSciences(title=title) for title in CRYOSPHERIC_SCIENCES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.EarthSciences.objects.bulk_create(
            [models.EarthSciences(title=title) for title in EARTH_SCIENCES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.BiologicalSciences.objects.bulk_create(
            [models.BiologicalSciences(title=title) for title in BIOLOGICAL_SCIENCES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.SocialSciencesAndHumanities.objects.bulk_create(
            [
                models.SocialSciencesAndHumanities(title=title)
                for title in SOCIAL_SCIENCES_AND_HUMANITIES_SUB_CATEGORIES
            ],
            ignore_conflicts=True
        )
        models.IntegratedSystems.objects.bulk_create(
            [models.IntegratedSystems(title=title) for title in INTEGRATED_SYSTEMS_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.SpatialScaleOfExpertise.objects.bulk_create(
            [models.SpatialScaleOfExpertise(title=title) for title in SPATIAL_SCALE_OF_EXPERTISE_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.StatisticalFocus.objects.bulk_create(
            [models.StatisticalFocus(title=title) for title in STATISTICAL_FOCUS_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.TimeScales.objects.bulk_create(
            [models.TimeScales(title=title) for title in TIME_SCALES_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.Methods.objects.bulk_create(
            [models.Methods(title=title) for title in METHODS_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.ParticipationInAssessments.objects.bulk_create(
            [models.ParticipationInAssessments(title=title) for title in PARTICIPATION_IN_ASSESSMENTS_SUB_CATEGORIES],
            ignore_conflicts=True
        )
        models.InputsOrParticipationToUNConventions.objects.bulk_create(
            [
                models.InputsOrParticipationToUNConventions(title=title)
                for title in INPUTS_OR_PARTICIPATION_TO_UN_CONVENTIONS_SUB_CATEGORIES
            ],
            ignore_conflicts=True
        )
        models.SpamFilterWord.objects.bulk_create(
            [models.SpamFilterWord(text=text) for text in SWISS_CHEESE],
            ignore_conflicts=True
        )
