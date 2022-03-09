from pipes import Template
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from .models import Question, QuestionComment
from answer.models import AnswerComment
from .forms import QuestionForm, QuestionCommentForm
from qbook.forms import SortForm
from django.shortcuts import redirect
from votes.models import QuestionDownVote, QuestionUpVote, AnswerDownVote, AnswerUpVote
from answer.forms import AnswerForm
from django.db.models import Count
from datetime import datetime, timezone
#Create your views here.
def QuestionFormView(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('login')
        form = QuestionForm()
    return render(request, 'question/question_form.html', {'form': form})

# class QuestionFormView(LoginRequiredMixin, CreateView):
#     model = Question
#     form_class = QuestionForm
#     template_name = 'question/question_form.html'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


def QuestionSingleView(request, pk):
    question = Question.objects.get(id=pk)
    question.views = question.views+1
    question.save()

    question_upvoted = False
    if QuestionUpVote.objects.filter(user=request.user, question=question).exists():
        question_upvoted = True

    question_downvoted = False
    if QuestionDownVote.objects.filter(user=request.user, question=question).exists():
        question_downvoted = True

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
    question.question_upvoted = question_upvoted
    question.question_downvoted = question_downvoted

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form1 = AnswerForm(request.POST)
        form2 = QuestionCommentForm(request.POST)
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
        if form2.is_valid():
            comment = form2.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
    form1 = AnswerForm()
    form2 = QuestionCommentForm()
    answers = question.answers.all()

    answers = answers.annotate(upvote=Count('upvotes'), downvote=Count('downvotes')).order_by('-upvote', 'downvote')

    for answer in answers:
        answer_date_diff = datetime.now(timezone.utc)-answer.date
        if answer_date_diff.days/365 > 1:
            answer_asked_long_ago = str(answer_date_diff.days/365) + ' years'
        elif answer_date_diff.days/30 > 1:
            answer_asked_long_ago = str(answer_date_diff.days/30) + ' months'
        elif answer_date_diff.days/7 > 1:
            answer_asked_long_ago = str(answer_date_diff.days/7) + ' weeks'   
        else:
            answer_asked_long_ago = str(answer_date_diff.days) + ' days'  
        answer.answer_asked_long_ago = answer_asked_long_ago

        answer_upvoted = False
        if AnswerUpVote.objects.filter(user=request.user, answer=answer).exists():
            answer_upvoted = True
            
        answer_downvoted = False
        if AnswerDownVote.objects.filter(user=request.user, answer=answer).exists():
            answer_downvoted = True

        answer.answer_upvoted = answer_upvoted
        answer.answer_downvoted = answer_downvoted

    question_comments = question.comments.all()

    for comment in question_comments:
        comment_date_diff = datetime.now(timezone.utc)-comment.date
        if comment_date_diff.days/365 > 1:
            comment_asked_long_ago = str(comment_date_diff.days/365) + ' years'
        elif comment_date_diff.days/30 > 1:
            comment_asked_long_ago = str(comment_date_diff.days/30) + ' months'
        elif comment_date_diff.days/7 > 1:
            comment_asked_long_ago = str(comment_date_diff.days/7) + ' weeks'   
        else:
            comment_asked_long_ago = str(comment_date_diff.days) + ' days'  
        comment.comment_asked_long_ago = comment_asked_long_ago

    return render(request, 'question/question_single.html', {'question': question, 'answers': answers, 'form1': form1, 'form2': form2, 'question_comments':question_comments})

def TagQuestionsView(request, tag):
    questions = Question.objects.filter(tag=tag).order_by('-date')

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
                    'questionupvote'), downvotes=Count('questiondownvote')).order_by('-views', '-upvotes', 'downvotes')
    else:
        form = SortForm()
    return render(request, 'question/tag_questions.html', {'questions': questions, 'tag': tag, 'form': form})


# class TagQuestionsView(FormMixin, ListView):
#     template_name = 'question/tag_questions.html'
#     form_class = SortForm

#     def get_queryset(self):
#         return Question.objects.filter(tag=self.kwargs['tag']).order_by('-date')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.form_class
#         context['questions'] = self.get_queryset()
#         return context

#     def form_valid(self, form, request, *args, **kwargs):
#         form_tag = form.cleaned_data['tag']
#         if form_tag == 'O':
#             self.queryset = self.get_queryset().order_by('date')
#         if form_tag == 'N':
#             self.queryset = self.get_queryset().order_by('-date')
#         if form_tag == 'P':
#             self.queryset = self.get_queryset().annotate(upvotes=Count(
#                 'questionupvote')).order_by('-views', '-upvotes' )

#         context = self.get_context_data(**kwargs)
#         context['form'] = self.form_class
#         context['questions'] = self.get_queryset()
#         return self.render_to_response(context)

class QuestionTagsView(TemplateView):
    template_name = 'question/question_tags.html'
    
# def QuestionEditView(request, pk):
#     question = Question.objects.get(id=pk)
#     if request.method == 'POST':
#         form = QuestionForm(request.POST, instance=question)
#         if form.is_valid():
#             form.save()
#             return redirect('question_single', pk=pk)
#     else:
#         form = QuestionForm(instance=question)
#     return render(request, 'question/question_edit.html', {'form': form})


class QuestionEditView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question/question_edit.html'


# def QuestionDeleteView(request, pk):
#     question = Question.objects.get(id=pk)
#     return render(request, 'question/question_delete.html', {'question': question})

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'question/question_delete.html'
    success_url = 'http://127.0.0.1:8000/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_object()
        return context

# def QuestionDeleteConfirmView(request, pk):
#     question = Question.objects.get(id=pk)
#     question.delete()
#     return redirect('home')

# def QuestionCommentDeleteView(request, pk):
#     comment = QuestionComment.objects.get(id=pk)
#     return render(request, 'question/question_comment_delete.html', {'comment': comment})

class QuestionCommentDeleteView(DeleteView):
    model = QuestionComment
    template_name = 'question/question_comment_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context

    def get_success_url(self):
        url = self.get_object().question.get_absolute_url()
        return url

# def QuestionCommentDeleteConfirmView(request, pk):
#     comment = QuestionComment.objects.get(id=pk)
#     comment.delete()
#     return redirect('question_single', pk=comment.question.id)


# def QuestionCommentEditView(request, pk):
#     comment = QuestionComment.objects.get(id=pk)
#     question = comment.question
#     if request.method == 'POST':
#         form = QuestionCommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('question_single', pk=question.id)
#     else:
#         form = QuestionCommentForm(instance=comment)
#     return render(request, 'question/question_comment_edit.html', {'form': form})

class QuestionCommentEditView(UpdateView):
    model = QuestionComment
    form_class = QuestionCommentForm
    template_name = 'question/question_comment_edit.html'

    def get_success_url(self):
        url = self.get_object().question.get_absolute_url()
        return url