from django.urls import path, include
from authentication.views import ResourceAPIView, GetListView, BillInvoice
from .models import Expense, BillTo, BillBy, BillDetail, BillItem
from .serializers import ExpenseSerializer, BillToSerializer, BillItemSerializer, BillDetailSerializer, BillBySerializer, BillToExpenseSerializer
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
        resource_serializer = BillDetailSerializer
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
]