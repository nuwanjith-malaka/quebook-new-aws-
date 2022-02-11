from django.contrib import admin
from django.urls import path
from .views import HomeView, TrendingView, SubscriptionsView, LatestQuestionsFeed
urlpatterns = [
    path('', HomeView, name='home'),
    path('trending/', TrendingView, name='trending'),
    path('subscriptions/', SubscriptionsView, name='subscriptions'),
    path('latest-questions/', LatestQuestionsFeed(), name='latest-questions'),
]