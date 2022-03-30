from rest_framework import serializers
from django.contrib. auth import get_user_model,authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate
from .models import Expense, BillTo, BillBy, BillDetail, BillItem, Dara
from django.db.models import Sum


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
class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = '__all__'


class BillDetailsSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='bill_by.name')
    party_name = serializers.CharField(source='bill_to.name')
    bill_items = BillItemSerializer(source='billitem_set', many=True) 

    class Meta:
        model = BillDetail
        fields = '__all__'

class BillDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='bill_by.name')
    party_name = serializers.CharField(source='bill_to.name')
    date = serializers.SerializerMethodField()
    bill_to = BillToSerializer()
    bill_by = BillBySerializer()
    bill_items = BillItemSerializer(source='billitem_set', many=True) 
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()

    class Meta:
        model = BillDetail
        fields = '__all__'
    
    def get_total_qty(self, obj):
        qty = obj.billitem_set.aggregate(Sum('qty'))
        return qty['qty__sum']
    
    def get_total_uom(self, obj):
        uom = obj.billitem_set.aggregate(Sum('uom'))
        return uom['uom__sum']
    def get_date(self,obj):
        return obj.date.strftime("%d %b %Y ")
class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillDetail
        fields = '__all__'


class DaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dara
        fields = '__all__'
class BillDetailinsideSerializer(serializers.ModelSerializer):
    bill_to = BillToExpenseSerializer()
    bill_by = BillBySerializer()
    class Meta:
        model = BillDetail
        fields = '__all__'