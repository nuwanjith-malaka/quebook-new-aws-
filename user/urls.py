from django.urls import path
from .views import  AskerView, EditProfileView, DeleteProfileView
urlpatterns = [
    path('editprofile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    path('deleteprofile/<int:pk>/', DeleteProfileView.as_view(), name='delete_profile'),
    path('askers/<int:pk>/', AskerView, name='asker'),
    # path('follow/<int:pk>/', UserFollowView, name='user_follow'),
]