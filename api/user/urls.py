from .views import AskerProfileView
from rest_framework.routers import DefaultRouter
from ..question.urls import router

router.register(r'users', AskerProfileView, basename='askers')
urlpatterns = router.urls