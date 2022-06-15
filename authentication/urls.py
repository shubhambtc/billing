from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView, ChangePasswordView, CheckAuthentication
urlpatterns = [
    path('users/check-authentication/',CheckAuthentication.as_view()),
    path('users/password/', ChangePasswordView.as_view()),
]