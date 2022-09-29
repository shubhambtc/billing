from django.urls import path, include
from .views import CheckAuthentication
from .csv_view import BillDetailCSV
urlpatterns = [
    path('users/check-authentication/',CheckAuthentication.as_view()),
    path('bulk-upload-bill',BillDetailCSV.as_view())
]