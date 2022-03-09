from django.shortcuts import render
from votes.models import QuestionUpVote, QuestionDownVote, AnswerUpVote, AnswerDownVote
from .serializers import QuestionUpVoteSerializer, QuestionDownVoteSerializer, AnswerUpVoteSerializer, AnswerDownVoteSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly

# Create your views here.

class QuestionUpVoteView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = QuestionUpVote.objects.all()
    serializer_class = QuestionUpVoteSerializer

class QuestionDownVoteView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = QuestionDownVote.objects.all()
    serializer_class = QuestionDownVoteSerializer

class AnswerUpVoteView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = AnswerUpVote.objects.all()
    serializer_class = AnswerUpVoteSerializer

class AnswerDownVoteView(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = AnswerDownVote.objects.all()
    serializer_class = AnswerDownVoteSerializer