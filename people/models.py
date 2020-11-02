from django.db import models

from ra.base.models import EntityModel, TransactionModel, TransactionItemModel, QuantitativeTransactionItemModel
from ra.base.registry import register_doc_type
from django.utils.translation import ugettext_lazy as _


class Topic(EntityModel):
    title = models.CharField(max_length=256)
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class Expertise(EntityModel):
    title = models.CharField(max_length=256)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = _('Expertise')
        verbose_name_plural = _('Expertise')



class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    OTHER = 'F', _('Female')
    FEMALE = 'O', _('Other')

class CareerStage(models.TextChoices):
    UNDERGRAD = 'UNDERGRAD', _("Undergraduate student (e.g. BSc/BA)")
    POSTGRAD = 'POSTGRAD', _("Postgraduate student (Masters/PhD student)")
    POSTDOC = 'POSTDOC', _("Postdoc/Junior Researcher")
    ACADEMIC = 'ACADEMIC', _("Academic (Senior Researcher, Professor)")
    PUBLICSECTOR = 'PUBLICSECTOR', _("Practitioner in the public/government sector")
    PRIVATESECTOR = 'PRIVATESECTOR', _("Practitioner or business in the private sector")
    OTHER = 'OTHER', _("Other (short text)")

class Person(EntityModel):
    orcid = models.CharField(max_length=128, unique=True,
        help_text="ORCID is a persistent unique digital identifier that you own and control")

    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    position = models.CharField(max_length=256)
    title = models.CharField(max_length=64)

    contact_email = models.CharField(max_length=256)
    personal_urls = models.TextField()
    upload_photo = models.FileField()

    career_stage_choice = models.CharField(max_length=16, choices=CareerStage.choices)
    career_stage_note = models.CharField(max_length=256)
    official_functions = models.TextField()

    expertise = models.ManyToManyField(
        Expertise,
        related_name="experts",
    )
    publications = models.TextField()

    allow_ecr = models.BooleanField(
        help_text="Would you like to be added to the ECR list of the MRI (applies for ECRs, <5 years from graduation)")
    allow_public = models.BooleanField(
        help_text="I allow publishing my profile on the web")
    allow_photo = models.BooleanField(
        help_text="I allow publishing my photo on the web")
    allow_contact = models.BooleanField(
        help_text="I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article).")
    allow_registry = models.BooleanField(
        help_text="I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by thor parties, journalists or collaborators of the MRI).")
    allow_newsletter = models.BooleanField(
        help_text="I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI")

    @property
    def fullname(self):
        namearray = []
        if self.title: namearray.push(self.title)
        if self.first_name: namearray.push(self.first_name)
        if self.last_name: namearray.push(self.last_name)
        return " ".join(namearray)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
