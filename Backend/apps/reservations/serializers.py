from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id', 'date', 'number_persons', 'state',
            'user', 'user_email',
            'service', 'service_title',
            'created_at'
        )
        read_only_fields = ('user', 'created_at')
