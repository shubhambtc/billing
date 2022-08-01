from django.urls import path, include
from .views import CheckAuthentication
urlpatterns = [
    path('users/check-authentication/',CheckAuthentication.as_view()),
]