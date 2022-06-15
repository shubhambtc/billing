from django.urls import path
from .models import Broker
from .serializers import BrokerSerializer
from authentication.views import ResourceAPIView, GetListView
urlpatterns = [
    path('broker/<int:pk>', ResourceAPIView.as_view(
        model=Broker,
        resource_serializer=BrokerSerializer
    )),
    path('broker-list/<str:page>', GetListView.as_view(
        model=Broker,
        resource_serializer=BrokerSerializer
    )),
]