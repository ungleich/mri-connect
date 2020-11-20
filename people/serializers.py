from rest_framework import serializers
from .models import Person, Affiliation, Topic, Expertise
from .util import expertiseByTopic

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    expertise = serializers.SerializerMethodField()

    def get_expertise(self, topic):
        """ Collapse expertise topics """
        return expertiseByTopic(
            Expertise.objects.filter(topic_id=topic.id).all()
        )[0]['expertise']

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
    topics = serializers.SerializerMethodField()
    publications = serializers.ReadOnlyField()

    expertise = ExpertiseSerializer(many=True, read_only=True)
    affiliation = AffiliationSerializer(read_only=True)

    class Meta:
        model = Person
        fields = (
            'id', 'date_edited',
            'fullname', 'last_name', 'first_name',

            'career', 'career_graduation',
            'position', 'official_functions',

            'url_cv', 'url_personal', 'url_researchgate',
            'url_publications', 'list_publications', 'publications',
            'url_photo',

            'topics',
            'expertise',
            'affiliation',
        )

    def get_url_photo(self, person):
        """ Fetch full link to a photo """
        request = self.context.get('request')
        if not person.upload_photo: return None
        url_photo = '/static/' + person.upload_photo.url
        return request.build_absolute_uri(url_photo)

    def get_topics(self, person):
        """ Collapse expertise topics """
        return expertiseByTopic(person.expertise.order_by('topic_id').all())
