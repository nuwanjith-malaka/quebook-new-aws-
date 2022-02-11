from django.shortcuts import render, redirect
from .models import Answer, AnswerComment
from .forms import AnswerForm, AnswerCommentForm
from question.forms import QuestionCommentForm
from question.forms import QuestionForm
from django.urls import reverse
from django.views.generic.edit import UpdateView, DeleteView,CreateView
# Create your views here.
# def AnswerEditView(request, pk):
#     if request.method == 'POST':
#         answer = Answer.objects.get(id=pk)
#         form = AnswerForm(request.POST, instance=answer)
#         if form.is_valid():
#             form.save()
#             return redirect('question_single', pk=answer.question.id)
#     else:
#         answer = Answer.objects.get(id=pk)
#         form = AnswerForm(instance=answer)
#     return render(request, 'answer/answer_edit.html', {'form': form})


class AnswerEditView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'answer/answer_edit.html'

    def get_success_url(self):
        return reverse('question_single', kwargs={'pk': self.get_object().question.pk})

# def AnswerDeleteView(request, pk):
#     answer = Answer.objects.get(id=pk)
#     return render(request, 'answer/answer_delete.html', {'answer': answer})


class AnswerDeleteView(DeleteView):
    model = Answer
    template_name = 'answer/answer_delete.html'
    

    def get_success_url(self):
        return reverse('question_single', kwargs={'pk': self.get_object().question.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer'] = self.get_object()
        return context


# def AnswerDeleteConfirmView(request, pk):
#     answer = Answer.objects.get(id=pk)
#     answer.delete()
#     return redirect('question_single', pk=answer.question.id)

# def AnswerCommentDeleteView(request, pk):
#     comment = AnswerComment.objects.get(id=pk)
#     return render(request, 'answer/answer_comment_delete.html', {'comment': comment})


class AnswerCommentDeleteView(DeleteView):
    model = AnswerComment
    template_name = 'answer/answer_comment_delete.html'
    

    def get_success_url(self):
        return reverse('question_single', kwargs={'pk': self.get_object().answer.question.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context


# def AnswerCommentDeleteConfirmView(request, pk):
#     comment = AnswerComment.objects.get(id=pk)
#     answer = comment.answer
#     comment.delete()
#     return redirect('question_single', pk=answer.question.id)


# def AnswerCommentEditView(request, pk):
#     comment = AnswerComment.objects.get(id=pk)
#     answer = comment.answer
#     if request.method == 'POST':
#         form = AnswerCommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('question_single', pk=answer.question.id)
#     else:
#         form = AnswerCommentForm(instance=comment)
#     return render(request, 'answer/answer_comment_edit.html', {'form': form})


class AnswerCommentEditView(UpdateView):
    model = AnswerComment
    form_class = AnswerCommentForm
    template_name = 'answer/answer_comment_edit.html'

    def get_success_url(self):
        return reverse('question_single', kwargs={'pk': self.get_object().answer.question.pk})


def AnswerCommentFormView(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    answer = Answer.objects.get(id=pk)
    if request.method == 'POST':
        form = AnswerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.answer = answer
            comment.save()
        return redirect('question_single', pk=answer.question.id)
    else:
        form = AnswerCommentForm()
    return render(request, 'answer/answer_comment_form.html', {'form': form})


# class AnswerCommentFormView(CreateView):
#     model = AnswerComment
#     form_class = AnswerCommentForm
#     template_name = 'answer/answer_comment_form.html'

#     def form_valid(self, form):
#         pk= self.kwargs['pk']
#         form.instance.user = self.request.user
#         form.instance.answer = Answer.objects.get(id=pk)
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('question_single', kwargs={'pk': self.get_object().answer.question.pk})

