from django.urls import path
from .views import QuestionFormView, QuestionSingleView, TagQuestionsView, QuestionTagsView, QuestionCommentEditView, QuestionCommentDeleteView, QuestionEditView, QuestionDeleteView 
urlpatterns = [
    path('questionform/', QuestionFormView, name='question_form'),
    path('question/<int:pk>/', QuestionSingleView, name='question_single'),
    path('questions/<tag>/', TagQuestionsView, name='tag_questions'),
    path('questionTags/', QuestionTagsView.as_view(), name='question_tags'),
    path('questioncommentedit/<int:pk>/',
         QuestionCommentEditView.as_view(), name='question_comment_edit'),
    path('questioncommentdelete/<int:pk>/',
         QuestionCommentDeleteView.as_view(), name='question_comment_delete'),
#     path('questioncommentdeleteconfirm/<int:pk>/',
#          QuestionCommentDeleteConfirmView, name='question_comment_delete_confirm'),
    path('questionedit/<int:pk>/', QuestionEditView.as_view(), name='question_edit'),
    path('questiondelete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),
#     path('questiondeleteconfirm/<int:pk>/',
#          QuestionDeleteConfirmView, name='question_delete_confirm'),
]