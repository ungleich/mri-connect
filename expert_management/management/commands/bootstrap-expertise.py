from django.core.management import BaseCommand

from expert_management import models


#FIXME: This looks very bad. Note to me to refactor it someday
class Command(BaseCommand):
    def handle(self, *args, **options):
        models.ResearchExpertise.objects.bulk_create([
            models.ResearchExpertise(title="Basic Research"),
            models.ResearchExpertise(title="Applied Research"),
            models.ResearchExpertise(title="Research Interface and Management"),
            models.ResearchExpertise(title="Interdisciplinary Research"),
            models.ResearchExpertise(title="Transdisciplinary Research"),
        ])
        models.AtmosphericSciences.objects.bulk_create([
            models.AtmosphericSciences(title="Meteorology"),
            models.AtmosphericSciences(title="Climatology"),
            models.AtmosphericSciences(title="Atmospheric Physics / Chemistry"),
            models.AtmosphericSciences(title="Pollution"),
        ])
        models.HydrosphericSciences.objects.bulk_create([
            models.HydrosphericSciences(title="Fresh Water Systems"),
            models.HydrosphericSciences(title="Precipitation and Runoff"),
            models.HydrosphericSciences(title="Hydrogeology"),
        ])
        models.CryosphericSciences.objects.bulk_create([
            models.CryosphericSciences(title="Glaciology"),
            models.CryosphericSciences(title="Snow Sciences"),
            models.CryosphericSciences(title="Permafrost and solifluction"),
        ])
        models.EarthSciences.objects.bulk_create([
            models.EarthSciences(title="Soil Science/Pedology"),
            models.EarthSciences(title="Geomorphology"),
            models.EarthSciences(title="Geochemistry"),
            models.EarthSciences(title="Geology"),
            models.EarthSciences(title="Physical Geography"),
            models.EarthSciences(title="Geophysics"),
        ])
        models.BiologicalSciences.objects.bulk_create([
            models.BiologicalSciences(title="Botany"),
            models.BiologicalSciences(title="Zoology"),
            models.BiologicalSciences(title="Ecology"),
            models.BiologicalSciences(title="Terrestrial Ecosystems"),
            models.BiologicalSciences(title="Aquatic Ecosystems"),
            models.BiologicalSciences(title="Soil organisms"),
            models.BiologicalSciences(title="Forestry"),
            models.BiologicalSciences(title="Ecosystem functioning"),
            models.BiologicalSciences(title="Ecosystem services"),
            models.BiologicalSciences(title="Biodiversity"),
        ])
        models.SocialSciencesAndHumanities.objects.bulk_create([
            models.SocialSciencesAndHumanities(title="History, classical studies, archaeology, prehistory and early history"),
            models.SocialSciencesAndHumanities(title="Linguistics and literature, philosophy"),
            models.SocialSciencesAndHumanities(title="Art studies, musicology, theatre and film studies, architecture"),
            models.SocialSciencesAndHumanities(title="Ethnology, social and human geography"),
            models.SocialSciencesAndHumanities(title="Psychology"),
            models.SocialSciencesAndHumanities(title="Educational studies"),
            models.SocialSciencesAndHumanities(title="Sociology, social work"),
            models.SocialSciencesAndHumanities(title="Political sciences"),
            models.SocialSciencesAndHumanities(title="Media and communication studies"),
            models.SocialSciencesAndHumanities(title="Public health"),
            models.SocialSciencesAndHumanities(title="Economics"),
            models.SocialSciencesAndHumanities(title="Law"),
        ])
        models.IntegratedSystems.objects.bulk_create([
            models.IntegratedSystems(title="Carbon Cycle"),
            models.IntegratedSystems(title="Other Biogeochemical Cycles"),
            models.IntegratedSystems(title="Hydrogeochemical Cycle"),
            models.IntegratedSystems(title="Nutrient Cycle"),
            models.IntegratedSystems(title="Social-ecological Systems"),
        ])
        models.SpatialScaleOfExpertise.objects.bulk_create([
            models.SpatialScaleOfExpertise(title="Global / Hemispheric"),
            models.SpatialScaleOfExpertise(title="Continental"),
            models.SpatialScaleOfExpertise(title="Regional"),
            models.SpatialScaleOfExpertise(title="National / Cultural"),
            models.SpatialScaleOfExpertise(title="Local / Community"),
        ])
        models.StatisticalFocus.objects.bulk_create([
            models.StatisticalFocus(title="Extremes"),
            models.StatisticalFocus(title="Mean Change / Trends"),
            models.StatisticalFocus(title="Variability"),
        ])
        models.TimeScales.objects.bulk_create([
            models.TimeScales(title="Seasonal / Annual"),
            models.TimeScales(title="Decadal / Centennial"),
            models.TimeScales(title="Millenial"),
            models.TimeScales(title="100 kyr"),
            models.TimeScales(title="Billenial (Mio yrs)"),
        ])
        models.Methods.objects.bulk_create([
            models.Methods(title="Earth Observations"),
            models.Methods(title="Remote sensing"),
            models.Methods(title="Field observations"),
            models.Methods(title="Field Experiments"),
            models.Methods(title="Modeling"),
            models.Methods(title="Spatial analysis"),
            models.Methods(title="Policy Analysis"),
            models.Methods(title="Qualitative social science methods"),
            models.Methods(title="Integrative assessments"),
            models.Methods(title="Synthesis and meta-analysis"),
        ])
        models.ParticipationInAssessments.objects.bulk_create([
            models.ParticipationInAssessments(title="IPCC"),
            models.ParticipationInAssessments(title="IPBES"),
            models.ParticipationInAssessments(title="UNDRR GAR"),
        ])
        models.InputsOrParticipationToUNConventions.objects.bulk_create([
            models.InputsOrParticipationToUNConventions(title="UN Agenda 2030 (SDGs) / UN HLPF"),
            models.InputsOrParticipationToUNConventions(title="UNFCCC"),
            models.InputsOrParticipationToUNConventions(title="CBD"),
            models.InputsOrParticipationToUNConventions(title="UNDRR Sedai"),
            models.InputsOrParticipationToUNConventions(title="UNCCD"),
        ])