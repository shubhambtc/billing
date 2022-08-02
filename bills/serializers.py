from rest_framework import serializers
from .models import BillTo, BillBy, BillDetail

def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

class BillToSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillTo
        fields = '__all__'

class BillToNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillTo
        fields = ('id','party_username')

class BillByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillBy
        fields = ('id','shortname')
class BillBySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillBy
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
    
    def get_total_bill_amount(self,obj):
        billitems = obj.billitems
        grand_total = 0
        total =0
        bags=0
        weights=0
        total_expenses = 0
        for billitem in billitems:
            total += billitem['qty']*billitem['rate']
            bags+=billitem['uom']
            weights+=billitem['qty']
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
    date = serializers.SerializerMethodField()
    class Meta:
        model = BillDetail
        fields = '__all__'
    
    def get_date(self,obj):
        return obj.date.strftime("%d %b %Y ")
    
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
    company_short_name = serializers.CharField(source='bill_by.shortname')
    party_username = serializers.CharField(source='bill_to.party_username')
    bill_tos = serializers.SerializerMethodField()
    bill_bys = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()
    total_exp = serializers.SerializerMethodField()
    class Meta:
        model = BillDetail
        exclude = ('invoice',)
    def get_total_exp(self,obj):
        billitems = obj.billitems
        total =0
        bags=0
        weights=0
        for billitem in billitems:
            total += billitem['qty']*billitem['rate']
            bags+=billitem['uom']
            weights+=billitem['qty']
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
        exp['total_expenses'] = round(sum(exp.values()),2)
        exp['grand_total'] = round_school(total+exp['total_expenses']+obj.frieght)
        return exp
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
