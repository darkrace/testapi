from django.contrib.auth.models import User
from rest_framework import serializers
from .models import WebexAuth

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class WebexAuthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebexAuth
        fields = '__all__'