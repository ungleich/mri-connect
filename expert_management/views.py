from functools import reduce
from itertools import chain

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import fields_for_model
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.gis.db.models import F, Value, Q, CharField
from django.db.models.functions import Concat
from django.contrib.postgres.search import SearchVector

from . import data
from .selector import get_user_profile
from .forms import ProjectForm, UserCreationForm, SearchForm, AdvanceSearchForm
from .models import Affiliation, Expertise, Project


class GoogleMapAPIKeyMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["google_map_api_key"] = settings.MAP_WIDGETS["GOOGLE_MAP_API_KEY"]
        return context


class Index(generic.TemplateView):
    template_name = "expert_management/index.html"


class MyProfileRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("profile", args=[self.request.user])


class Signup(generic.CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class Profile(GoogleMapAPIKeyMixin, generic.DetailView):
    queryset = get_user_model().objects.all()
    pk_url_kwarg = "username"
    template_name = "expert_management/profile.html"

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.pk_url_kwarg)
        return get_user_profile(username, self.request.user)


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    template_name = "expert_management/set-profile.html"
    success_url = reverse_lazy("my-profile")

    fields = fields_for_model(model, exclude=data.AUTH_SPECIFIC_FIELDS)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectList(GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class CreateProject(GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    template_name = "expert_management/set-project.html"
    success_url = reverse_lazy("projects")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProject(GoogleMapAPIKeyMixin, LoginRequiredMixin, generic.UpdateView):
    form_class = ProjectForm
    template_name = "expert_management/set-project.html"
    success_url = reverse_lazy("projects")

    def get_queryset(self, queryset=None):
        if queryset is None:
            queryset = Project.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy("projects")

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class CreateExpertise(LoginRequiredMixin, generic.CreateView):
    model = Expertise
    fields = fields_for_model(model, exclude={'user'})
    template_name = "expert_management/set-expertise.html"
    success_url = reverse_lazy("my-profile")

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


class UpdateExpertise(LoginRequiredMixin, generic.UpdateView):
    model = Expertise
    fields = fields_for_model(model, exclude={'user'})
    template_name = "expert_management/set-expertise.html"
    success_url = reverse_lazy("my-profile")

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


class Search(generic.TemplateView):
    template_name = "expert_management/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        return context


class AdvanceSearch(generic.TemplateView):
    template_name = "expert_management/advance-search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvanceSearchForm
        return context


def transform_tt(string):
    return string.replace(" ", "_")

def Q_if_truthy(**kwargs):
    q = Q(**kwargs)
    truthy = reduce(lambda x, y: x and bool(y), dict(q.children).values(), True)
    return (q if truthy else Q())


class SearchResultView(generic.ListView):
    template_name = "expert_management/search-result.html"
    model = get_user_model()

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        expertise = self.request.GET.get("expertise", "")
        regions_of_expertise = self.request.GET.getlist("regions_of_expertise", [])
        regions_of_interest = self.request.GET.getlist("regions_of_interest", [])
        official_functions = self.request.GET.get("official_functions", "")
        career_stages = self.request.GET.getlist("career_stage", [])
        affiliation = self.request.GET.get("affiliation", "")
        country = self.request.GET.get("country", "")

        other_expertise_fields = ["other_expertise", "other_spatial_scale_of_expertise", "other_statistical_focus", "other_time_scales", "other_methods", "other_participation_in_assessments", "more_detail_about_participation_in_assessments", "other_inputs_or_participation_to_un_conventions"]

        queryset = get_user_model().objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
        expertise_fields = [
            f"expertise__{field}__overlap" for field in fields_for_model(Expertise, exclude=other_expertise_fields + ["user", "mountain_ranges_of_research_interest", "other_mountain_ranges_of_research_interest", "mountain_ranges_of_research_expertise", "other_mountain_ranges_of_research_expertise" ])
        ]

        q = Q()

        for field in expertise_fields:
            q |= Q_if_truthy(**{field: [expertise]})

        for field in map(lambda s: f"expertise__{s}__icontains", other_expertise_fields):
            q |= Q_if_truthy(**{field: expertise})

        q |= Q_if_truthy(full_name__icontains=name)
        q |= Q_if_truthy(official_functions__icontains=official_functions)
        q |= Q_if_truthy(affiliations__name__icontains=affiliation)
        q |= Q_if_truthy(affiliations__country=country)
        q |= Q_if_truthy(projects__country=country)

        for region in regions_of_expertise:
            q |= Q_if_truthy(expertise__mountain_ranges_of_research_expertise__name=region)
            q |= Q_if_truthy(expertise__other_mountain_ranges_of_research_expertise__icontains=region)

        for region in regions_of_interest:
            q |= Q_if_truthy(expertise__mountain_ranges_of_research_interest__name=region)
            q |= Q_if_truthy(expertise__other_mountain_ranges_of_research_interest__icontains=region)

        for career_stage in career_stages:
            q |= Q_if_truthy(career_stage=career_stage)

        q &= Q_if_truthy(is_public=True)

        return queryset.filter(q).distinct()
