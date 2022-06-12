from rest_framework import serializers
from django.contrib. auth import get_user_model,authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate
from .models import Expense, BillTo, BillBy, BillDetail, BillItem, Dara
from django.db.models import Sum

def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

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
    class Meta:
        model = BillDetail
        fields = '__all__'

class BillDetailListSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='bill_to.name')
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()
    total_bill_amount = serializers.SerializerMethodField()
    class Meta:
        model = BillDetail
        fields = ('id','invoice_no','party_name','total_qty','total_uom','vehicle_no','total_bill_amount','date')
    
    def get_total_qty(self, obj):
        qty = obj.billitem_set.aggregate(Sum('qty'))
        return qty['qty__sum']
    
    def get_total_uom(self, obj):
        uom = obj.billitem_set.aggregate(Sum('uom'))
        return uom['uom__sum']
    def get_total_bill_amount(self,obj):
        billitems = obj.billitem_set.all()
        grand_total = 0
        total =0
        bags=0
        weights=0
        total_expenses = 0
        for billitem in billitems:
            total += billitem.qty*billitem.rate
            bags+=billitem.uom
            weights+=billitem.qty
        if obj.bill_to==4:
            weights=bags
        expenses = obj.expenses
        exp = {}
        exp['tulai'] = round(expenses['tulai']*total/100,2) if expenses else 0
        exp['dharmada'] = round(expenses['dharmada']*total/100,2) if expenses else 0
        exp['wages'] = round(expenses['wages']*weights,2) if expenses else 0
        exp['sutli'] = round(expenses['sutli']*bags,2) if expenses else 0
        exp['commision'] = round(expenses['commision']*total/100,2) if expenses else 0
        exp['loading_charges'] = round(expenses['loading_charges']*bags,2) if expenses else 0
        exp['vikas_shulk'] = round(expenses['vikas_shulk']*total/100,2) if expenses else 0
        exp['mandi_shulk'] = round(expenses['mandi_shulk']*total/100,2) if expenses else 0
        exp['bardana'] = round(expenses['bardana']*bags,2) if expenses else 0
        exp['others'] = round(expenses['others'],2) if expenses else 0
        total_expenses = round(sum(exp.values()),2)
        grand_total = round_school(total+total_expenses+obj.frieght)
        return grand_total


class ForPrintingBillSerializer(serializers.ModelSerializer):
    bill_tos = serializers.SerializerMethodField()
    bill_bys = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()

    class Meta:
        model = BillDetail
        fields = '__all__'
    
    def get_total_qty(self, obj):
        billitems = obj.billitems
        qty=0
        for billitem in billitems:
            qty +=billitem['qty']
        return qty
    
    def get_total_uom(self, obj):
        billitems = obj.billitems
        uom=0
        for billitem in billitems:
            uom +=billitem['uom']
        return uom
    def get_bill_tos(self,obj):
        return BillToSerializer(obj.bill_to).data
    def get_bill_bys(self,obj):
        return BillBySerializer(obj.bill_by).data
    
    class Meta:
        model = BillDetail
        fields = '__all__'


class BillDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='bill_by.name')
    party_name = serializers.CharField(source='bill_to.name')
    bill_tos = serializers.SerializerMethodField()
    bill_bys = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()

    class Meta:
        model = BillDetail
        fields = '__all__'
    
    def get_total_qty(self, obj):
        billitems = obj.billitems
        qty=0
        for billitem in billitems:
            qty +=billitem['qty']
        return qty
    
    def get_total_uom(self, obj):
        billitems = obj.billitems
        uom=0
        for billitem in billitems:
            uom +=billitem['uom']
        return uom
    def get_bill_tos(self,obj):
        return BillToSerializer(obj.bill_to).data
    def get_bill_bys(self,obj):
        return BillBySerializer(obj.bill_by).data

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