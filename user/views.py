from django.urls import reverse
from django.shortcuts import render, redirect
from votes.models import QuestionDownVote, QuestionUpVote
from question.models import Question
from .models import AskerProfile, FriendShip
from django.contrib.auth.models import User
from .forms import AskerProfileForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
# Create your views here.
def AskerView(request, pk):
    user = User.objects.get(id=pk)
    questions = Question.objects.filter(user=user)
    for question in questions:
        question.upvotes = QuestionUpVote.objects.filter(
            question=question).count()
        question.downvotes = QuestionDownVote.objects.filter(
            question=question).count()
    if request.method == 'POST':
        form = AskerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            asker_profile = form.save(commit=False)
            asker_profile.user = request.user
            asker_profile.save()
        return redirect('asker', pk=pk)
    else:
        try:
            asker = AskerProfile.objects.get(user=user)
            context = {
                'questions': questions,
                'asker': asker,

            }
            return render(request, 'user/asker.html', context)
        except AskerProfile.DoesNotExist:
            if request.user == user:
                form = AskerProfileForm()
                context = {
                    'questions': questions,
                    'form': form,
                    'user': user

                }
            else:
                context = {
                    'questions': questions,
                    'user': user

                }
            return render(request, 'user/asker.html', context)

# def EditProfileView(request, pk):
#     asker = AskerProfile.objects.get(id=pk)
#     user = asker.user
#     if request.method == 'POST':
#         form = AskerProfileForm(request.POST, request.FILES, instance=asker)
#         if form.is_valid():
#             form.save()
#             return redirect('asker', pk=user.pk)
#     else:
#         form = AskerProfileForm(instance=asker)
#     return render(request, 'user/edit_profile.html', {'form': form, 'asker': asker, 'user': user})


class EditProfileView(UpdateView):
    model = AskerProfile
    form_class = AskerProfileForm
    template_name = 'user/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['user'] = self.get_object().user
        return context


# def DeleteProfileView(request, pk):
#     user = AskerProfile.objects.get(pk=pk).user
#     if request.method == 'POST':
#         user.delete()
#         return redirect('home')
#     return render(request, 'user/delete_profile.html', {'user': user})


class DeleteProfileView(DeleteView):
    model = AskerProfile
    template_name = 'user/delete_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asker'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user.delete()
        return HttpResponseRedirect(success_url)


# def UserFollowView(request, pk):
#     asker = User.objects.get(pk=pk)
#     FriendShip.objects.create(to_user=asker, from_user=request.user)
#     return redirect('asker', pk=pk)