from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'people', PeopleViewSet)
router.register(r'search', SearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
