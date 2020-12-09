from django.urls import path

from .views import Profile

urlpatterns = [
    path('user/<str:username>/', Profile.as_view(), name='profile')
]
