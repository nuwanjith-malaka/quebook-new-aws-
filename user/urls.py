from django.urls import path
from .views import  AddFriendView, UnFriendView, AskerView, ConfirmRequestView, DeleteRequestView, EditProfileView, DeleteProfileView, FriendsView
urlpatterns = [
    path('editprofile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    path('deleteprofile/<int:pk>/', DeleteProfileView.as_view(), name='delete_profile'),
    path('askers/<int:pk>/', AskerView, name='asker'),
    path('friends/', FriendsView, name='friends'),
    path('addfriend/<int:pk>/', AddFriendView, name='add_friend'),
    path('unfriend/<int:pk>/', UnFriendView, name='un_friend'),
    path('confirmrequest/<int:pk>/', ConfirmRequestView, name='confirm_request'),
    path('deleterequest/<int:pk>/', DeleteRequestView, name='delete_request'),
]