from django.urls import path
from .models import LoadingUnloading, OrderParty, Purchaseorder, SalesOrder, PartyBardanaBalance
from .serializers import LoadingSerializer, OrderPartySerializer, SalesOrderSerializer, PurchaseorderSerializer,DetailedPurchaseOrderSerializer,DetailedSalesOrderSerializer, DetailedUnloadingSerializer, BardanaBalanceSerializer
from authentication.views import ResourceAPIView, GetListView
from .views import GetPendingSalesOrder, LoadingResourceView, GetPendingOrder, UnloadingResourceView, OrderDasboard, BardanaOptionsView
urlpatterns = [
    path('get-purchase-orders/<int:pk>',GetPendingOrder.as_view()),
    path('get-sales-orders/<int:pk>',GetPendingSalesOrder.as_view()),
    path('party/<int:pk>', ResourceAPIView.as_view(
        model=OrderParty,
        resource_serializer=OrderPartySerializer
    )),
    path('party-list/<str:page>', GetListView.as_view(
        model=OrderParty,
        resource_serializer=OrderPartySerializer,
        search_fields = ["name","email","contact_number"]
    )),
    path('sales/<int:pk>', ResourceAPIView.as_view(
        model=SalesOrder,
        resource_serializer=SalesOrderSerializer
    )),
    path('sales-list/<str:page>', GetListView.as_view(
        model=SalesOrder,
        resource_serializer=SalesOrderSerializer,
        search_fields = ["party__name","genes","broker__name"]
    )),
    path('purchase/<int:pk>', ResourceAPIView.as_view(
        model=Purchaseorder,
        resource_serializer=PurchaseorderSerializer
    )),
    path('detailed-sales/<int:pk>', ResourceAPIView.as_view(
        model=SalesOrder,
        resource_serializer=DetailedSalesOrderSerializer
    )),
    path('detailed-purchase/<int:pk>', ResourceAPIView.as_view(
        model=Purchaseorder,
        resource_serializer=DetailedPurchaseOrderSerializer
    )),
    path('detailed-unloading/<int:pk>', ResourceAPIView.as_view(
        model=LoadingUnloading,
        resource_serializer=DetailedUnloadingSerializer
    )),
    path('purchase-list/<str:page>', GetListView.as_view(
        model=Purchaseorder,
        resource_serializer=PurchaseorderSerializer,
        search_fields = ["party__name","genes","broker__name",]
    )),
    path('loading/<int:pk>', LoadingResourceView.as_view()),
    path('unloading/<int:pk>', UnloadingResourceView.as_view()),
    path('loading-list/<str:page>', GetListView.as_view(
        model=LoadingUnloading,
        resource_serializer=LoadingSerializer,
        search_fields = ["genes","vehicle_number","bill_or_builty"]
    )),
    path('bardana-balance-list/<str:page>', GetListView.as_view(
        model=PartyBardanaBalance,
        resource_serializer=BardanaBalanceSerializer
    )),
    path('bardana-options/<int:pk>', BardanaOptionsView.as_view()),
    path('dashboard',OrderDasboard.as_view()),
]