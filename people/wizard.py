import data_wizard
from rest_framework import serializers
from .models import *

data_wizard.register(Person)
data_wizard.register(Expertise)

class PersonSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(source='last_name')
    FirstName = serializers.CharField(source='first_name')
    EMailAddress = serializers.CharField(source='contact_email')
    UnivCompAbbr = serializers.PrimaryKeyRelatedField(
                        read_only=True, source='affiliation')

    def create(self, val):
        print(val)
        obj = super(PersonSerializer, self).create(val)
        # find or create affiliation
        a_name = val['affiliation']
        a_obj = Affiliation.objects.get(name=a_name)
        if not a_obj:
            a_obj = AffiliationSerializer().create(
                name=a_name
            )
        obj.affiliation = a_obj
        return obj

    class Meta:
        model = Person
        fields = ('Name','FirstName','EMailAddress','UnivCompAbbr')
        data_wizard = {
            'header_row': 0,
            'start_row': 1,
            'show_in_list': True,
            'idmap': data_wizard.idmap.always,
        }

data_wizard.register("ProClim Import", PersonSerializer)
