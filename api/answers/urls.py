from .views import AnswerView, AnswerCommentView
from rest_framework.routers import DefaultRouter
from ..question.urls import router

router.register(r'answers', AnswerView, basename='answers')
router.register(r'answerComments', AnswerCommentView, basename='answer_comments')
urlpatterns = router.urls