from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import User


def get_user_profile(username: str, requester: User):
    is_owner_requesting = username == requester.username

    profile = get_object_or_404(get_user_model(), username=username)

    if is_owner_requesting:
        return profile

    if not profile.is_photo_public:
        # FIXME: It is not working yet.
        profile.picture = None

    if profile.is_public:
        return profile

    raise Http404()
