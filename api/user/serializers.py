from rest_framework import serializers
from user.models import AskerProfile

class AskerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskerProfile
        fields = '__all__'