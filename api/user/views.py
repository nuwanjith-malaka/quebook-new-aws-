from django.shortcuts import render
from user.models import AskerProfile
from .serializers import AskerProfileSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly

# Create your views here.

class AskerProfileView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = AskerProfile.objects.all()
    serializer_class = AskerProfileSerializer