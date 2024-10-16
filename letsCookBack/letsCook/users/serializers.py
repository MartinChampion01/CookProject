from django.contrib.auth.models import Group, User
from rest_framework import serializers

#Va permettre la sérialisation d'objet python en JSON pour la communication pas les APIs

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
