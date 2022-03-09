from django.contrib import admin
from django.urls import path
from .views import HomeView, LatestQuestionsView
urlpatterns = [
    path('', HomeView, name='home'),
    path('latestQuestions/', LatestQuestionsView, name='latest'),
]