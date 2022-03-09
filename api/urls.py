from django.urls import path, include
from api.question import urls as question_urls
from api.user import urls as user_urls
from api.answers import urls as answer_urls
from api.votes import urls as vote_urls
# from .views import api_root

urls = vote_urls.urlpatterns + answer_urls.urlpatterns + user_urls.urlpatterns + question_urls.urlpatterns

urlpatterns = [
    path(r'api/', include(urls))
]