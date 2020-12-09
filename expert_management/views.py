from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets

from .models import Expert
from .serializers import *


class Signup(generic.CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "/accounts/login/"


class Profile(generic.DetailView):
    queryset = Expert.objects.all().prefetch_related('projects')
    pk_url_kwarg = "username"
    template_name = "expert_management/profile.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.queryset
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            obj = queryset.get(user=get_object_or_404(get_user_model(), username=pk))
        except Expert.DoesNotExist:
            return None
        else:
            return obj

    def render_to_response(self, context, **response_kwargs):
        if not context['object']:
            return HttpResponse(f"The profile for \"{self.kwargs.get(self.pk_url_kwarg)}\" does not exists yet! If it is your profile, please wait while we create the view/page to let you create a profile")
        return super().render_to_response(context, **response_kwargs)
