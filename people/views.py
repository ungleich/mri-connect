from rest_framework import viewsets, filters
from .models import Person, Topic
from .serializers import *

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(allow_public=True).all()
    serializer_class = PersonSerializer


# class AdvancedSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         return request.GET.getlist('fields', [])

class SearchViewSet(viewsets.ModelViewSet):
    search_fields = ['last_name', 'first_name', 'position', 'official_functions']
    filter_backends = (filters.SearchFilter,)
    # filter_backends = (AdvancedSearchFilter,)
    queryset = Person.objects.filter(allow_public=True).order_by('-date_edited').all()
    serializer_class = SearchSerializer


class TopicViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
