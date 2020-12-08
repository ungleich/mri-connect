from rest_framework import serializers
from .models import Expert, Affiliation, Expertise
# from .util import expertiseByTopic

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'

# class TopicSerializer(serializers.ModelSerializer):
#     expertise = serializers.SerializerMethodField()

#     def get_expertise(self, topic):
#         """ Collapse expertise topics """
#         return expertiseByTopic(
#             Expertise.objects.filter(topic_id=topic.id).all()
#         )[0]['expertise']

#     class Meta:
#         model = Topic
#         fields = '__all__'

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ('id', 'last_name', 'first_name', 'location')

class ExpertSerializer(serializers.ModelSerializer):
    url_photo = serializers.SerializerMethodField()
    # topics = serializers.SerializerMethodField()
    publications = serializers.ReadOnlyField()

    expertise = ExpertiseSerializer(many=True, read_only=True)
    affiliation = AffiliationSerializer(read_only=True)

    class Meta:
        model = Expert
        fields = (
            'id', 'date_edited',
            'fullname', 'last_name', 'first_name',

            'career', 'year_of_last_degree_graduation',
            'position', 'official_functions',

            'url_cv', 'url_personal', 'url_researchgate',
            'url_publications', 'list_publications', 'publications',
            'url_photo',

            # 'topics',
            'expertise',
            'affiliations',
        )

    def get_url_photo(self, expert):
        """ Fetch full link to a photo """
        request = self.context.get('request')
        if not expert.upload_photo: return None
        url_photo = '/static/' + expert.upload_photo.url
        return request.build_absolute_uri(url_photo)

    # def get_topics(self, expert):
    #     """ Collapse expertise topics """
    #     return expertiseByTopic(expert.expertise.order_by('topic_id').all())
