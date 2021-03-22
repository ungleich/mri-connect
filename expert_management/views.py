import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.db.models import F, Q, Value
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.functions import Concat
from django.forms.models import ModelMultipleChoiceField, fields_for_model
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic

from . import data
from .forms import (AdvancedSearchForm, AffiliationForm, ContactForm,
                    CustomUserCreationForm, ExpertiseForm, ProfileForm,
                    ProjectForm, SearchForm)
from .models import Affiliation, Expertise, Project, User
from .selector import get_user_profile
from .utils.common import Q_if_truthy, non_zero_keys
from .utils.importdata import classify_expertise
from .utils.mailchimp import Mailchimp

logger = logging.getLogger(__name__)


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.title})
        return context


class GoogleMapAPIKeyMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["google_map_api_key"] = settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]
        return context


class Index(TitleMixin, generic.TemplateView):
    template_name = "expert_management/index.html"
    title = "Homepage"


class MyProfileRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("profile", args=[self.request.user.username])


class Signup(TitleMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    title = "Signup"


class Profile(GoogleMapAPIKeyMixin, generic.DetailView):
    queryset = get_user_model().objects.all()
    pk_url_kwarg = "username"
    template_name = "expert_management/profile.html"

    def get_context_data(self, **kwargs):
        user = self.get_object()
        full_name = " ".join([user.first_name, user.last_name])

        context = super().get_context_data(**kwargs)
        context.update({'title': full_name})
        return context

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.pk_url_kwarg)
        return get_user_profile(username, self.request.user)


class UpdateProfile(TitleMixin, LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    template_name = "expert_management/set-profile.html"
    success_url = reverse_lazy("my-profile")
    title = "Update Profile"
    form_class = ProfileForm
    # fields = fields_for_model(model, exclude=data.AUTH_SPECIFIC_FIELDS)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        mailchimp = Mailchimp()

        # NOTE: We can do little optimization here i.e checking whether is_subscribed_to_newsletter
        # changed or not. and if changed then we can update the mailchimp. We can check that using
        # if 'is_subscribed_to_newsletter' in form.changed_data but it have some quirky behavior and
        # I do not want to optimize it prematurely

        if form.instance.user.is_subscribed_to_newsletter:
            mailchimp.add_member(form.instance.user.email, settings.MAILCHIMP_LIST_ID)
        else:
            mailchimp.delete_member(form.instance.user.email, settings.MAILCHIMP_LIST_ID)

        return super().form_valid(form)


class ProjectList(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.ListView):
    title = "My Projects"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class CreateProject(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    template_name = "expert_management/set-project.html"
    success_url = reverse_lazy("projects")
    title = "Create Project"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProject(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.UpdateView):
    form_class = ProjectForm
    template_name = "expert_management/set-project.html"
    success_url = reverse_lazy("projects")
    title = "Update Project"

    def get_queryset(self, queryset=None):
        if queryset is None:
            queryset = Project.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteProject(TitleMixin, LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy("projects")
    title = "Confirm Project Deletion"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class AffiliationList(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.ListView):
    title = "My Affiliations (created by me)"

    def get_queryset(self):
        return Affiliation.objects.filter(creator=self.request.user)


class CreateAffiliation(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.CreateView):
    form_class = AffiliationForm
    template_name = "expert_management/set-affiliation.html"
    success_url = reverse_lazy("affiliations")
    title = "Create Affiliation"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateAffiliation(TitleMixin, GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.UpdateView):
    form_class = AffiliationForm
    template_name = "expert_management/set-affiliation.html"
    success_url = reverse_lazy("affiliations")
    title = "Update Affiliation"

    def get_queryset(self, queryset=None):
        if queryset is None:
            queryset = Affiliation.objects.filter(creator=self.request.user)
        return queryset

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CreateExpertise(TitleMixin, LoginRequiredMixin, generic.CreateView):
    model = Expertise
    form_class = ExpertiseForm
    template_name = "expert_management/set-expertise.html"
    success_url = reverse_lazy("my-profile")
    title = "Update Expertise"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            self.model.objects.get(user=self.request.user)
        except self.model.DoesNotExist:
            return super().get(*args, **kwargs)
        else:
            return redirect('update-expertise')


class UpdateExpertise(TitleMixin, LoginRequiredMixin, generic.UpdateView):
    model = Expertise
    form_class = ExpertiseForm
    template_name = "expert_management/set-expertise.html"
    success_url = reverse_lazy("my-profile")
    title = "Update Expertise"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.model.objects.filter(user=self.request.user)
        return queryset.get(user=self.request.user)

    def get(self, *args, **kwargs):
        try:
            self.model.objects.get(user=self.request.user)
        except self.model.DoesNotExist:
            return redirect('create-expertise')
        else:
            return super().get(*args, **kwargs)


class Search(TitleMixin, generic.TemplateView):
    template_name = "expert_management/search.html"
    title = 'Search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        return context


class AdvancedSearch(TitleMixin, generic.TemplateView):
    template_name = "expert_management/advanced-search.html"
    title = 'Advanced Search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvancedSearchForm
        return context


class SearchResultView(TitleMixin, generic.ListView):
    template_name = "expert_management/search-result.html"
    model = get_user_model()
    title = "Search Result"

    def get_queryset(self):
        other_expertise_fields = [
            "other_expertise", "other_spatial_scale_of_expertise", "other_statistical_focus",
            "other_time_scales", "other_methods", "other_participation_in_assessments",
            "more_detail_about_participation_in_assessments", "other_inputs_or_participation_to_un_conventions",
            "other_mountain_ranges_of_research_interest", "other_mountain_ranges_of_research_expertise"
        ]
        expertise_fields = fields_for_model(
            Expertise,
            exclude=other_expertise_fields + [
                "user",
                "mountain_ranges_of_research_expertise",
                "mountain_ranges_of_research_interest"
            ]
        )

        name = self.request.GET.get("name", "")
        expertise = self.request.GET.getlist("expertise", [])
        regions_of_expertise = self.request.GET.getlist("mountain_ranges_of_research_expertise", [])
        regions_of_interest = self.request.GET.getlist("mountain_ranges_of_research_interest", [])
        official_functions = self.request.GET.get("official_functions", "")
        career_stages = self.request.GET.getlist("career_stage", [])
        affiliation = self.request.GET.get("affiliation", "")
        country = self.request.GET.get("country", "")

        form_data = non_zero_keys({
            field_name: self.request.GET.get(field_name, "") if not isinstance(field, ModelMultipleChoiceField)
                                                             else self.request.GET.getlist(field_name, [])
            for field_name, field in expertise_fields.items()
        } if not expertise else classify_expertise(expertise))

        queryset = get_user_model().objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
        query = Q()

        for field in form_data:
            query |= Q_if_truthy(**{f"expertise__{field}__title__in": form_data[field]})

        for field in map(lambda s: f"expertise__{s}__icontains", other_expertise_fields):
            query |= Q_if_truthy(**{field: " ".join(expertise)})

        query |= Q_if_truthy(full_name__icontains=name)
        query |= Q_if_truthy(official_functions__icontains=official_functions)
        query |= Q_if_truthy(affiliations__name__icontains=affiliation)
        query |= Q_if_truthy(affiliations__country=country)
        query |= Q_if_truthy(projects__country=country)
        query |= Q_if_truthy(career_stage__in=career_stages)

        query |= Q_if_truthy(expertise__mountain_ranges_of_research_expertise__name__in=regions_of_expertise)
        query |= Q_if_truthy(
            expertise__other_mountain_ranges_of_research_expertise__icontains=" ".join(regions_of_expertise)
        )

        query |= Q_if_truthy(expertise__mountain_ranges_of_research_interest__name__in=regions_of_interest)
        query |= Q_if_truthy(
            expertise__other_mountain_ranges_of_research_interest__icontains=" ".join(regions_of_interest)
        )

        return queryset.filter(query & Q(is_public=True)).distinct() if query else queryset.none()


class Contact(TitleMixin, generic.FormView):
    template_name = "expert_management/contact.html"
    form_class = ContactForm
    title = "Contact"
    success_url = "contact"

    def get_success_url(self):
        return reverse_lazy("contact", args=[self.kwargs["username"]])

    def get(self, request, *args, **kwargs):
        get_object_or_404(User, username=kwargs["username"]).email
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email, body, *_ = form.cleaned_data.values()
        self.send_email(email, body)
        return super().form_valid(form)

    def send_email(self, email, body):
        try:
            recepient_email = get_object_or_404(User, username=self.kwargs["username"]).email
            email = EmailMessage(
                subject=f'Message from {get_current_site(self.request).name}',
                body=body,
                to=[recepient_email],
                reply_to=[email]
            )
            email.send(fail_silently=False)
        except Exception as e:
            logger.exception(e)
            messages.add_message(self.request, messages.ERROR, 'An error occurred while sending email', 'danger')
        else:
            messages.add_message(self.request, messages.SUCCESS, 'Message sent successfully')
