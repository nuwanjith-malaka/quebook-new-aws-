from  django.urls import path 
from .views import QuestionUpVoteView, QuestionDownVoteView, AnswerUpVoteView, AnswerDownVoteView
urlpatterns = [
    path('questionupvote/<int:pk>/', QuestionUpVoteView, name='questionupvote'),
    path('questiondownvote/<int:pk>/',
         QuestionDownVoteView, name='questiondownvote'),
    path('answerupvote/<int:pk>/', AnswerUpVoteView, name='answerupvote'),
    path('answerdownvote/<int:pk>/', AnswerDownVoteView, name='answerdownvote'),
]