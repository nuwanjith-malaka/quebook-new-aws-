from .views import QuestionUpVoteView, QuestionDownVoteView, AnswerUpVoteView, AnswerDownVoteView
from rest_framework.routers import DefaultRouter
from ..question.urls import router

router.register(r'questionUpVotes', QuestionUpVoteView, basename='question_upvotes')
router.register(r'questionDownVotes', QuestionDownVoteView, basename='question_downvotes')
router.register(r'answerUpVotes', AnswerUpVoteView, basename='answer_upvotes')
router.register(r'answerDownVotes', AnswerDownVoteView, basename='answer_downvotes')
urlpatterns = router.urls