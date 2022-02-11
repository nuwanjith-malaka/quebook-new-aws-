from django.shortcuts import render
from django.shortcuts import redirect
from question.models import Question
from .models import AnswerDownVote, AnswerUpVote, QuestionUpVote, QuestionDownVote
from answer.models import Answer
# Create your views here.
def QuestionUpVoteView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    question = Question.objects.get(id=pk)
    try:
        upvote = QuestionUpVote.objects.get(
            user=request.user, question=question)
        return redirect('question_single', pk=pk)
    except QuestionUpVote.DoesNotExist:
        QuestionUpVote.objects.create(user=request.user, question=question)
        return redirect('question_single', pk=pk)


def QuestionDownVoteView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    question = Question.objects.get(id=pk)
    try:
        downvote = QuestionDownVote.objects.get(
            user=request.user, question=question)
        return redirect('question_single', pk=pk)
    except QuestionDownVote.DoesNotExist:
        QuestionDownVote.objects.create(user=request.user, question=question)
        return redirect('question_single', pk=pk)

def AnswerUpVoteView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    answer = Answer.objects.get(id=pk)
    try:
        upvote = AnswerUpVote.objects.get(user=request.user, answer=answer)
        return redirect('question_single', pk=answer.question.id)
    except AnswerUpVote.DoesNotExist:
        AnswerUpVote.objects.create(user=request.user, answer=answer)
        return redirect('question_single', pk=answer.question.id)


def AnswerDownVoteView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    answer = Answer.objects.get(id=pk)
    try:
        downvote = AnswerDownVote.objects.get(user=request.user, answer=answer)
        return redirect('question_single', pk=answer.question.id)
    except AnswerDownVote.DoesNotExist:
        AnswerDownVote.objects.create(user=request.user, answer=answer)
        return redirect('question_single', pk=answer.question.id)