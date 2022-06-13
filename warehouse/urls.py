from django.urls import path
from authentication.views import ResourceAPIView
urlpatterns = [
    path('', ResourceAPIView.as_view(
    )),
]