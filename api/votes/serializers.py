from rest_framework import serializers
from votes.models import QuestionUpVote, QuestionDownVote, AnswerUpVote, AnswerDownVote

class QuestionUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionUpVote
        fields = '__all__'

class QuestionDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionDownVote
        fields = '__all__'

class AnswerUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerUpVote
        fields = '__all__'

class AnswerDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerDownVote
        fields = '__all__'