from rest_framework import serializers
from .models import BillTo, BillBy, BillDetail, Bilty

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
class ConsignorSerializer(serializers.ModelSerializer):

    class Meta:
        model=BillBy
        fields = ('name','id','bilty_add','gstin')

class ConsigneeSerializer(serializers.ModelSerializer):
    delivery_at = serializers.SerializerMethodField()
    class Meta:
        model=BillTo
        fields = ('name','id','delivery_at','gstin')
    
    def get_delivery_at(self,obj):
        return obj.ship_details['address']

class ForPrintingBiltySerializer(serializers.ModelSerializer):
    consignee = serializers.SerializerMethodField()
    consignor = serializers.SerializerMethodField()
    net_qty = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    all_up = serializers.SerializerMethodField()
    bilty_info = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    class Meta:
        model = BillDetail
        fields = ('consignee','consignor','net_qty','uom','qty','frieght_per_qtl','bilty_info','bilty_type','item','frieght','all_up','date','invoice_no')
    def get_item(self,obj):
        return obj.billitems[0]['item']
    def get_all_up(self,obj):
        d = obj.date.strftime("%d %b %Y ")
        c = {
            "date": d,
            "vehicle_no":obj.vehicle_no,
            "num":"123",
        }
        return c
    def get_bilty_info(self,obj):
        bilty = BiltySerializer(obj.bill_by.bilty).data
        return bilty
        
    def get_net_qty(self, obj):
        billitems = obj.billitems
        qty=0
        for billitem in billitems:
            qty +=billitem['net_qty']
        return qty
    
    def get_qty(self, obj):
        billitems = obj.billitems
        qty=0
        for billitem in billitems:
            qty +=billitem['qty']
        return qty
    
    def get_uom(self, obj):
        billitems = obj.billitems
        uom=0
        for billitem in billitems:
            uom +=billitem['uom']
        return uom
    def get_consignee(self,obj):
        return ConsigneeSerializer(obj.bill_to).data
    def get_consignor(self,obj):
        return ConsignorSerializer(obj.bill_by).data

class ForPrintingBillSerializer(serializers.ModelSerializer):
    bill_tos = serializers.SerializerMethodField()
    bill_bys = serializers.SerializerMethodField()
    total_qty = serializers.SerializerMethodField()
    total_uom = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    class Meta:
        model = BillDetail
        fields = '__all__'
    def get_bilty_info(self,obj):
        bilty = BiltySerializer(obj.bill_by.bilty).data
        return bilty
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


class BiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilty
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
        expenses = obj.expenses
        exp = {}
        arr = [0,bags,weights,total/100] 
        exp['tulai'] = round(expenses['tulai']*arr[int(expenses['tulai_s'])],2) if expenses else 0
        exp['dharmada'] = round(expenses['dharmada']*arr[int(expenses['dharmada_s'])],2) if expenses else 0
        exp['wages'] = round(expenses['wages']*arr[int(expenses['wages_s'])],2) if expenses else 0
        exp['sutli'] = round(expenses['sutli']*arr[int(expenses['sutli_s'])],2) if expenses else 0
        exp['commision'] = round(expenses['commision']*arr[int(expenses['commision_s'])],2) if expenses else 0
        exp['loading_charges'] = round(expenses['loading_charges']*arr[int(expenses['loading_charges_s'])],2) if expenses else 0
        exp['vikas_shulk'] = round(expenses['vikas_shulk']*arr[int(expenses['vikas_shulk_s'])],2) if expenses else 0
        exp['mandi_shulk'] = round(expenses['mandi_shulk']*arr[int(expenses['mandi_shulk_s'])],2) if expenses else 0
        exp['bardana'] = round(expenses['bardana']*arr[int(expenses['bardana_s'])],2) if expenses else 0
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
