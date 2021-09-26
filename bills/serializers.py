from rest_framework import serializers
from django.contrib. auth import get_user_model,authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate
from .models import Expense, BillTo, BillBy, BillDetail, BillItem


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class BillToSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillTo
        fields = '__all__'

class BillToExpenseSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer()
    class Meta:
        model = BillTo
        fields = '__all__'

class BillBySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillBy
        fields = '__all__'

class BillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = '__all__'

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = '__all__'


class BillDetailinsideSerializer(serializers.ModelSerializer):
    bill_to = BillToExpenseSerializer()
    bill_by = BillBySerializer()
    class Meta:
        model = BillDetail
        fields = '__all__'