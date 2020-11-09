from rest_framework import serializers
from .models import Person, Affiliation


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    affiliation = AffiliationSerializer(read_only=True)
    url_photo = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'date_edited',
            'last_name',
            'first_name',
            'fullname',
            'position',
            'career',
            'career_graduation',
            'official_functions',
            'url_photo',
            'url_cv',
            'url_personal',
            'url_publications',
            'url_researchgate',
            'list_publications',

            'affiliation',
        )

    def get_url_photo(self, person):
        request = self.context.get('request')
        url_photo = person.upload_photo.url
        return request.build_absolute_uri(url_photo)
