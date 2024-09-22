from rest_framework import serializers
from base.models import Room

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # Use 'all' to dynamically get all fields in the model
        fields = '__all__'
