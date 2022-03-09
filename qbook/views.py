from django.shortcuts import render
from question.models import Question
from .forms import SortForm
from django.db.models import Count
from votes.models import QuestionUpVote, QuestionDownVote
from datetime import datetime, timezone
from user.models import FriendShip
from django.db.models import Q
from django.shortcuts import redirect
# Create your views here.

def HomeView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    to_friends = [friendship.from_user for friendship in FriendShip.objects.filter(to_user=request.user, accepted=True)]
    from_friends = [friendship.to_user for friendship in FriendShip.objects.filter(from_user=request.user, accepted=True)]
    friends = to_friends + from_friends + [request.user]
    questions = Question.objects.filter(Q(user__in=friends)).order_by('-date')
    for question in questions:
        question_date_diff = datetime.now(timezone.utc)-question.date
        if question_date_diff.days/365 > 1:
            question_asked_long_ago = str(question_date_diff.days/365) + ' years'
        elif question_date_diff.days/30 > 1:
            question_asked_long_ago = str(question_date_diff.days/30) + ' months'
        elif question_date_diff.days/7 > 1:
            question_asked_long_ago = str(question_date_diff.days/7) + ' weeks'   
        else:
            question_asked_long_ago = str(question_date_diff.days) + ' days'  
        question.question_asked_long_ago = question_asked_long_ago

    return render(request, 'qbook/home.html', {'questions':questions})


def LatestQuestionsView(request):
    questions = Question.objects.all().order_by('-date')
    for question in questions:
        question_date_diff = datetime.now(timezone.utc)-question.date
        if question_date_diff.days/365 > 1:
            question_asked_long_ago = str(question_date_diff.days/365) + ' years'
        elif question_date_diff.days/30 > 1:
            question_asked_long_ago = str(question_date_diff.days/30) + ' months'
        elif question_date_diff.days/7 > 1:
            question_asked_long_ago = str(question_date_diff.days/7) + ' weeks'   
        else:
            question_asked_long_ago = str(question_date_diff.days) + ' days'  
        question.question_asked_long_ago = question_asked_long_ago

    return render(request, 'qbook/latest.html', {'questions': questions})