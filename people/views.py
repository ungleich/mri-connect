from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Person, Topic
from .serializers import *


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PeopleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.filter(allow_public=True).all()
    serializer_class = PersonSerializer

class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    search_fields = ['last_name', 'first_name', 'position', 'official_functions']
    filter_backends = (filters.SearchFilter,)
    # filter_backends = (AdvancedSearchFilter,)
    queryset = Person.objects.filter(allow_public=True).order_by('-date_edited').all()
    serializer_class = SearchSerializer

# class AdvancedSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         return request.GET.getlist('fields', [])

class ExpertiseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.filter(allow_public=True).order_by('last_name').all()
    serializer_class = SearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['expertise']
