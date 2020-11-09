from django.urls import include, path
from rest_framework import routers
from .views import PeopleViewSet, PeopleAdvancedViewSet

router = routers.DefaultRouter()
router.register(r'people', PeopleViewSet)
router.register(r'advanced', PeopleAdvancedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
