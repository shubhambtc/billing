from django.urls import path
from authentication.views import ResourceAPIView, GetListView, Bill, getcsv,getbillwisecsv,getbillwithexpensecsv, GetDataUpdated, BillResourceAPIView
from .models import Expense, BillTo, BillBy, BillDetail, BillItem, Dara
from .serializers import ExpenseSerializer, BillToSerializer, BillItemSerializer, BillBySerializer, DaraSerializer, BillDetailsSerializer,BillDetailListSerializer
urlpatterns = [
    path('expense/<int:pk>', ResourceAPIView.as_view(
        model = Expense,
        resource_serializer = ExpenseSerializer
    )),
    path('expense-list/<str:page>',GetListView.as_view(
        model = Expense,
        resource_serializer = ExpenseSerializer
    )),
    path('bill-to/<int:pk>', ResourceAPIView.as_view(
        model = BillTo,
        resource_serializer = BillToSerializer
    )),
    path('bill-to-list/<str:page>',GetListView.as_view(
        model = BillTo,
        resource_serializer = BillToSerializer,
        search_fields = ["name","gstin"]
    )),
    path('bill-by/<int:pk>', ResourceAPIView.as_view(
        model = BillBy,
        resource_serializer = BillBySerializer
    )),
    path('bill-by-list/<str:page>',GetListView.as_view(
        model = BillBy,
        resource_serializer = BillBySerializer
    )),
    path('bill-detail/<int:pk>', BillResourceAPIView.as_view(
        model = BillDetail,
        resource_serializer = BillDetailsSerializer
    )),
    path('bill-details-list/<str:page>',GetListView.as_view(
        model = BillDetail,
        resource_serializer = BillDetailListSerializer,
        search_fields=["invoice_no"],
        search_fields_bill = ["invoice_no","vehicle_no","date","bill_to__name","bill_by__name"]
    )),
    path('bill-detail-list/<str:page>',GetListView.as_view(
        model = BillDetail,
        resource_serializer = BillDetailsSerializer,
        search_fields=["invoice_no"],
        search_fields_bill = ["invoice_no","vehicle_no","date","bill_to__name","bill_by__name"]
    )),
    path('bill-item/<int:pk>', ResourceAPIView.as_view(
        model = BillItem,
        resource_serializer = BillItemSerializer
    )),
    path('bill-item-list/<str:page>',GetListView.as_view(
        model = BillItem,
        resource_serializer = BillItemSerializer
    )),
    path('dara/<int:pk>', ResourceAPIView.as_view(
        model = Dara,
        resource_serializer = DaraSerializer
    )),
    path('dara-list/<str:page>',GetListView.as_view(
        model = Dara,
        resource_serializer = DaraSerializer
    )),
    path('bill-get/<int:pk>',Bill.as_view()),
    path('bill-csv/<int:pk>',getcsv.as_view()),
    path('bill-wise-csv/<int:pk>',getbillwisecsv.as_view()),
    path('bill-wise-expense-csv/<int:pk>',getbillwithexpensecsv.as_view()),
    path('edit',GetDataUpdated.as_view()),
]
