from django.shortcuts import render
from answer.models import Answer, AnswerComment
from .serializers import AnswerSerializer, AnswerCommentSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly

# Create your views here.

class AnswerView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerCommentView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = AnswerComment.objects.all()
    serializer_class = AnswerCommentSerializer