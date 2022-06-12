from django.urls import path
from authentication.views import ResourceAPIView, GetListView
from .models import Party, Warehouse
from .serializers import PartySerializer, WarehouseSerializer
urlpatterns = [
    path('party/<int:pk>', ResourceAPIView.as_view(
        model = Party,
        resource_serializer = PartySerializer
    )),
    path('party-list/<str:page>',GetListView.as_view(
        model = Party,
        resource_serializer = PartySerializer
    )),
    path('warehouse/<int:pk>', ResourceAPIView.as_view(
        model = Warehouse,
        resource_serializer = WarehouseSerializer
    )),
    path('warehouse-list/<str:page>',GetListView.as_view(
        model = Warehouse,
        resource_serializer = WarehouseSerializer
    )),
]