from .views import QuestionView, QuestionCommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'questions', QuestionView, basename='questions')
router.register(r'questionComments', QuestionCommentView, basename='question_comments')
urlpatterns = router.urls