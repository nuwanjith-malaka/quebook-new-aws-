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
#Create your views here.
# def QuestionFormView(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.user = request.user
#             question.save()
#             return redirect('home')
#     if request.method == 'GET':
#         if not request.user.is_authenticated:
#             return redirect('login')
#         form = QuestionForm()
#     return render(request, 'question/question_form.html', {'form': form})

class QuestionFormView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question/question_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def QuestionSingleView(request, pk):
    question = Question.objects.get(id=pk)
    question.upvotes = QuestionUpVote.objects.filter(question=question).count()
    question.downvotes = QuestionDownVote.objects.filter(
        question=question).count()
    question.views = question.views+1
    question.save()
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
    answers = question.answer_set.all()
    # for answer in answers:
    #     answer.upvotes = AnswerUpVote.objects.filter(answer=answer).count()
    #     answer.downvotes = AnswerDownVote.objects.filter(answer=answer).count()
    #     answer.comments = AnswerComment.objects.filter(answer=answer)
    comments = question.questioncomment_set.all()
    answers = answers.annotate(upvotes=Count(
                    'answerupvote'), downvotes=Count('answerdownvote')).order_by('-upvotes', 'downvotes')
    for answer in answers:
        answer.comments = AnswerComment.objects.filter(answer=answer)
    return render(request, 'question/question_single.html', {'question': question, 'answers': answers, 'form1': form1, 'form2': form2, 'comments': comments})

def TagQuestionsView(request, tag):
    questions = Question.objects.filter(tag=tag).order_by('-date')
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
                    'questionupvote')).order_by('-views', '-upvotes' )
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