from rest_framework import serializers
from .models import  OrderParty,SalesOrder,Purchaseorder, LoadingUnloading, LoadingOrders, UnloadingOrders

class OrderPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderParty
        fields="__all__"
class LoadingSerializer(serializers.ModelSerializer):
    loading_from_type = serializers.CharField(source='loading_from.party_type',read_only=True)
    loading_from_name = serializers.SerializerMethodField()
    unloading_from_name = serializers.SerializerMethodField()
    class Meta:
        model = LoadingUnloading
        fields="__all__"
    def get_loading_from_name(self,obj):
        lst=[]
        for loading in obj.loading_from.all():
            dic={}
            dic['label'] = loading.name
            dic['value'] = loading.id
            dic['val'] = loading.party_type
            lst.append(dic)
        return lst
    def get_unloading_from_name(self,obj):
        lst=[]
        for loading in obj.unloaded_to.all():
            dic={}
            dic['label'] = loading.name
            dic['value'] = loading.id
            dic['val'] = loading.party_type
            lst.append(dic)
        return lst

class LoadingOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadingOrders
        fields="__all__"


class UnloadingOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnloadingOrders
        fields="__all__"


class SalesOrderSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    party_contact_number = serializers.CharField(source='party.contact_number',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    broker_contact_number = serializers.CharField(source='broker.contact_number',read_only=True)
    class Meta:
        model = SalesOrder
        fields="__all__"
    
    def update(self, instance, validated_data):
        if instance.quantity != validated_data['quantity']:
            validated_data['pending'] = instance.pending+(validated_data['quantity']-instance.quantity)
        
        return super().update(instance, validated_data)
class PurchaseorderInsideSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    class Meta:
        model = Purchaseorder
        fields=('id','date','party_name','party','broker_name','broker','quantity','pending','rate','unit')

class SalesOrderInsideSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    class Meta:
        model = SalesOrder
        fields=('id','date','party_name','party','broker_name','broker','quantity','pending','rate','unit')
class PurchaseorderSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    party_contact_number = serializers.CharField(source='party.contact_number',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    broker_contact_number = serializers.CharField(source='broker.contact_number',read_only=True)
    class Meta:
        model = Purchaseorder
        fields="__all__"

    def update(self, instance, validated_data):
        if instance.quantity != validated_data['quantity']:
            validated_data['pending'] = instance.pending+(validated_data['quantity']-instance.quantity)
        
        return super().update(instance, validated_data)


class DetailedPurchaseOrderSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    party_contact_number = serializers.CharField(source='party.contact_number',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    broker_contact_number = serializers.CharField(source='broker.contact_number',read_only=True)
    loadings = serializers.SerializerMethodField()
    class Meta:
        model = Purchaseorder
        fields="__all__"

    def get_loadings(self,obj):
        loading_orders = LoadingOrders.objects.filter(purchase_order=obj,is_active=True)
        lst=[]
        for loading in loading_orders:
            dic={
                "date":loading.loading.date,
                "vehicle_number":loading.loading.vehicle_number,
                "quantity_loaded":loading.quantity_loaded,
                "quantity":loading.quantity,
            }
            lst.append(dic)
        return lst

class DetailedSalesOrderSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name',read_only=True)
    party_contact_number = serializers.CharField(source='party.contact_number',read_only=True)
    broker_name = serializers.CharField(source='broker.name',read_only=True)
    broker_contact_number = serializers.CharField(source='broker.contact_number',read_only=True)
    unloadings = serializers.SerializerMethodField()
    class Meta:
        model = SalesOrder
        fields="__all__"

    def get_unloadings(self,obj):
        unloading_orders = UnloadingOrders.objects.filter(sales_order=obj,is_active=True)
        lst=[]
        for unloading in unloading_orders:
            dic={
                "date":unloading.loading.unloading_date,
                "vehicle_number":unloading.loading.vehicle_number,
                "quantity_unloaded":unloading.quantity_unloaded,
                "quantity":unloading.quantity,
            }
            lst.append(dic)
        return lst

class DetailedUnloadingSerializer(serializers.ModelSerializer):
    loading_from_name = serializers.SerializerMethodField()
    unloading_from_name = serializers.SerializerMethodField()
    unloadings = serializers.SerializerMethodField()
    loadings = serializers.SerializerMethodField()
    class Meta:
        model = LoadingUnloading
        fields="__all__"
    def get_loading_from_name(self,obj):
        lst=[]
        for loading in obj.loading_from.all():
            dic={}
            dic['label'] = loading.name
            dic['value'] = loading.id
            dic['val'] = loading.party_type
            lst.append(dic)
        return lst
    def get_unloading_from_name(self,obj):
        lst=[]
        for loading in obj.unloaded_to.all():
            dic={}
            dic['label'] = loading.name
            dic['value'] = loading.id
            dic['val'] = loading.party_type
            lst.append(dic)
        return lst
    
    def get_unloadings(self,obj):
        lst=[]
        for unloading in obj.unloading.all():
            dic={}
            try:
                dic['party'] = unloading.unloading_party.name
            except:
                dic['party'] = None
            try:
                dic['broker'] =  unloading.unloading_broker.name
            except:
                dic['broker'] = None
            dic['quantity_unloaded'] = unloading.quantity_unloaded
            dic['quantity'] = unloading.quantity
            dic['rate'] = unloading.sales_order.rate
            dic['condition'] = unloading.sales_order.condition
            print(dic)
            lst.append(dic)
        return lst

    def get_loadings(self,obj):
        lst=[]
        for loading in obj.loadingorders_set.all():
            dic={}
            try:
                dic['party'] = loading.loading_party.name
            except:
                dic['party'] = None
            try:
                dic['broker'] = loading.loading_broker.name
            except:
                dic['broker'] = None
            dic['quantity_loaded'] = loading.quantity_loaded
            dic['quantity'] = loading.quantity
            dic['rate'] = loading.purchase_order.rate
            dic['condition'] = loading.purchase_order.condition
            lst.append(dic)
        return lst


