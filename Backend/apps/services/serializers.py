from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Service
        fields = ('id', 'title', 'description', 'image')
