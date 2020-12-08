from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register(r'topics', TopicViewSet)
router.register(r'expert', ExpertViewSet)
router.register(r'search', SearchViewSet)
router.register(r'advanced', AdvancedViewSet)
router.register(r'expertise', ExpertiseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # url(r'activate/', 'expert_management.views.')
]
