from django.urls import path, include
from authentication.views import ResourceAPIView, GetListView, BillInvoice, Bill, getcsv,getbillwisecsv,getbillwithexpensecsv, DeleteBill,BillEdit
from .models import Expense, BillTo, BillBy, BillDetail, BillItem, Dara
from .serializers import ExpenseSerializer, BillToSerializer, BillItemSerializer, BillDetailSerializer, BillBySerializer, BillToExpenseSerializer, BillSerializer, DaraSerializer
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
        resource_serializer = BillToExpenseSerializer
    )),
    path('bill-by/<int:pk>', ResourceAPIView.as_view(
        model = BillBy,
        resource_serializer = BillBySerializer
    )),
    path('bill-by-list/<str:page>',GetListView.as_view(
        model = BillBy,
        resource_serializer = BillBySerializer
    )),
    path('bill-detail/<int:pk>', ResourceAPIView.as_view(
        model = BillDetail,
        resource_serializer = BillSerializer
    )),
    path('bill-detail-list/<str:page>',GetListView.as_view(
        model = BillDetail,
        resource_serializer = BillDetailSerializer
    )),
    path('bill-create', BillInvoice.as_view()),
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
    path('bill-delete/<int:pk>',DeleteBill.as_view()),
    path('bill-edit/<int:pk>',BillEdit.as_view())
]
