from django.shortcuts import render
from question.models import Question
from .forms import SortForm
from django.db.models import Count
from votes.models import QuestionUpVote, QuestionDownVote
# Create your views here.
def HomeView(request):
    questions = Question.objects.all().order_by('-date')
    if request.method == 'POST':
        form = SortForm(request.POST)
        if form.is_valid():
            form_tag = form.cleaned_data['tag']
            if form_tag == 'O':
                questions = questions.order_by('date')
            if form_tag == 'N':
                questions = questions.order_by('-date')
            if form_tag == 'P':
                questions = questions.annotate(upvotes=Count(
                    'questionupvote')).order_by('-views', '-upvotes')
    else:
        form = SortForm()
    return render(request, 'qbook/home.html', {'questions': questions, 'form': form})


def TrendingView(request):
    questions = Question.objects.all()
    for question in questions:
        question.upvotes = QuestionUpVote.objects.filter(
            question=question).count()
        question.downvotes = QuestionDownVote.objects.filter(
            question=question).count()
    return render(request, 'qbook/trending.html', {'questions': questions})


def SubscriptionsView(request):
    questions = Question.objects.all()
    for question in questions:
        question.upvotes = QuestionUpVote.objects.filter(
            question=question).count()
        question.downvotes = QuestionDownVote.objects.filter(
            question=question).count()
    return render(request, 'qbook/subscriptions.html', {'questions': questions})

from django.contrib.syndication.views import Feed
from django.urls import reverse
from question.models import Question

class LatestQuestionsFeed(Feed):
    title = "Latest questions"
    link = "/sitenews/"
    description = "Latest questions askeed by users."

    def items(self):
        return Question.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.tag

    def item_description(self, item):
        return item.body

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('question_single', args=[item.pk])