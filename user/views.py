from django.urls import reverse
from django.shortcuts import render, redirect
from votes.models import QuestionDownVote, QuestionUpVote
from question.models import Question
from .models import AskerProfile, FriendShip
from django.contrib.auth.models import User
from .forms import AskerProfileForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from datetime import datetime, timezone
# Create your views here.
def AskerView(request, pk):
    user = User.objects.get(id=pk)
    questions = Question.objects.filter(user=user)

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

def FriendsView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        asker_profile = AskerProfile.objects.get(user=request.user)
        user = User.objects.get(pk=request.user.pk)
    except AskerProfile.DoesNotExist:
        return redirect('asker', request.user.pk)
    
    to_friends = [friendship.from_user.asker for friendship in FriendShip.objects.filter(to_user=user, accepted=True)]
    from_friends = [friendship.to_user.asker for friendship in FriendShip.objects.filter(from_user=user, accepted=True)]
    friends_requested = [friendship.from_user.asker for friendship in FriendShip.objects.filter(to_user=user, accepted=False)]
    requested_friends = [friendship.to_user.asker for friendship in FriendShip.objects.filter(from_user=user, accepted=False)]

    sugession_1 = AskerProfile.objects.filter(school=asker_profile.school, city=asker_profile.city, grade=asker_profile.grade).exclude(user=user)
    sugession_2 = AskerProfile.objects.filter(school=asker_profile.school, grade=asker_profile.grade).exclude(city=asker_profile.city)
    sugession_3 = AskerProfile.objects.filter(school=asker_profile.school, city=asker_profile.city).exclude(grade=asker_profile.grade)
    sugession_4 = AskerProfile.objects.filter(city=asker_profile.city, grade=asker_profile.grade).exclude(school=asker_profile.school)
    sugession_5 = AskerProfile.objects.filter(school=asker_profile.school).exclude(grade=asker_profile.grade).exclude(city=asker_profile.city)
    sugession_6 = AskerProfile.objects.filter(city=asker_profile.city).exclude(school=asker_profile.school).exclude(grade=asker_profile.grade)
    
    askers = list(AskerProfile.objects.all().exclude(user=user))

    from itertools import chain
    sugessions = list(chain(sugession_1, sugession_2, sugession_3, sugession_4, sugession_5, sugession_6))
    askers = list(set(askers) - set(sugessions)- set(requested_friends) - set(to_friends) - set(from_friends))
    sugessions = list(set(sugessions) - set(requested_friends)- set(to_friends) - set(from_friends))
    
    return render(request, 'user/friends.html', {'askers':askers, 'from_friends':from_friends, 'to_friends':to_friends, 'friends_requested':friends_requested, 'requested_friends':requested_friends, 'sugessions':sugessions})

# class FriendsView(TemplateView):
#     template_name = 'user/friends.html'

def AddFriendView(request, pk):
    to_user = User.objects.get(pk=pk)
    try:
        friendship = FriendShip.objects.get(from_user=request.user, to_user=to_user, accepted=False)
        friendship.delete()
    except FriendShip.DoesNotExist:
        friendship = FriendShip.objects.create(from_user=request.user, to_user=to_user, accepted=False)
    return redirect('friends')

def UnFriendView(request, pk):
    user = User.objects.get(pk=pk)
    try:
        friendship = FriendShip.objects.get(from_user=request.user, to_user=user, accepted=True)
    except FriendShip.DoesNotExist:
        friendship = FriendShip.objects.get(from_user=user, to_user=request.user, accepted=True)
    friendship.delete()
    return redirect('friends')

def ConfirmRequestView(request, pk):
    from_user = User.objects.get(pk=pk)
    friendship = FriendShip.objects.get(to_user=request.user, from_user=from_user)
    friendship.accepted = True
    friendship.save()
    return redirect('friends')

def DeleteRequestView(request, pk):
    from_user = User.objects.get(pk=pk)
    friendship = FriendShip.objects.get(to_user=request.user, from_user=from_user)
    friendship.delete()
    return redirect('friends')