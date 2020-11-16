from rest_framework import serializers
from .models import Person, Affiliation, Topic, Expertise


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'last_name', 'first_name', 'location')

class PersonSerializer(serializers.ModelSerializer):
    url_photo = serializers.SerializerMethodField()
    affiliation = AffiliationSerializer(read_only=True)
    expertise = ExpertiseSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'id', 'date_edited',
            'fullname', 'last_name', 'first_name',

            'career', 'career_graduation',
            'position', 'official_functions',

            'url_photo',
            'url_cv', 'url_personal', 'url_researchgate',
            'url_publications', 'list_publications',

            'affiliation',
            'expertise',
        )

    def get_url_photo(self, person):
        request = self.context.get('request')
        if not person.upload_photo: return None
        url_photo = person.upload_photo.url
        return request.build_absolute_uri(url_photo)
