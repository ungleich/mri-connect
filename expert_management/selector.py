from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.gis.db.models import Value, ImageField

from .models import User


def get_user_profile(username: str, requester: User):
    is_owner_requesting = username == requester.username
    try:
        profile = get_user_model().objects.values().get(username=username)
    except get_user_model().DoesNotExist:
        raise Http404()

    if profile['photo'] == '' or not (profile['is_photo_public'] or is_owner_requesting):
        profile['photo'] = ImageField()
        profile['photo'].url = lambda: 'https://miro.medium.com/max/720/1*W35QUSvGpcLuxPo3SRTH4w.png'

    if is_owner_requesting:
        return User(**profile)

    if profile['is_public']:
        return User(**profile)

    raise Http404()
