from itertools import permutations
from django.shortcuts import render
from question.models import Question, QuestionComment
from .serializers import QuestionSerializer, QuestionCommentSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly
# Create your views here.

class QuestionView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCommentView(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentSerializer