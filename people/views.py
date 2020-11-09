from rest_framework import viewsets, filters
from .models import Person
from .serializers import PersonSerializer

class PeopleViewSet(viewsets.ModelViewSet):
    search_fields = ['last_name', 'first_name', 'position', 'official_functions']
    filter_backends = (filters.SearchFilter,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class AdvancedSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('fields', [])


class PeopleAdvancedViewSet(viewsets.ModelViewSet):
    filter_backends = (AdvancedSearchFilter,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
