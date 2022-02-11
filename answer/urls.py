from django.urls import path
from .views import  AnswerCommentDeleteView, AnswerCommentEditView, AnswerEditView, AnswerDeleteView, AnswerCommentFormView
urlpatterns = [
    path('answercommentedit/<int:pk>/',
         AnswerCommentEditView.as_view(), name='answer_comment_edit'),     
    path('answercommentform/<int:pk>/',
         AnswerCommentFormView, name='answer_comment_form'), 
    path('answeredit/<int:pk>/', AnswerEditView.as_view(), name='answer_edit'),
    path('answerdelete/<int:pk>/', AnswerDeleteView.as_view(), name='answer_delete'),
#     path('answerdeleteconfirm/<int:pk>/',
#          AnswerDeleteConfirmView, name='answer_delete_confirm'),
    path('answercommentdelete/<int:pk>/',
         AnswerCommentDeleteView.as_view(), name='answer_comment_delete'),
#     path('answercommentdeleteconfirm/<int:pk>/',
#          AnswerCommentDeleteConfirmView, name='answer_comment_delete_confirm'),
 ]