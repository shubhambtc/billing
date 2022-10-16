from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from bills.models import BillTo
from .models import LoadingOrders, LoadingUnloading, PartyBardanaBalance, Purchaseorder, SalesOrder, UnloadingOrders
from .serializers import BardanaBalanceSerializer, LoadingOrdersSerializer, LoadingSerializer, PurchaseorderSerializer, PurchaseorderInsideSerializer, UnloadingOrdersSerializer, SalesOrderInsideSerializer
from django.db.models import Sum
# Create your views here.

class GetPendingOrder(APIView):

    def get(self, request, pk):
        dict1={}
        dict1['is_active']=True
        for k, v in request.query_params.items():
            fieldValue=v
            if k.endswith('__in'):
                fieldValue = request.query_params.getlist(k)
            dict1[k] = fieldValue
        try:
            party_params = dict1["party__in"]
            dict2 = {
                "loading": pk,
                "loading_party__in":party_params
            }
        except:
            pass
        try:
            broker_params = dict1["broker__in"]
            dict2 = {
                "loading": pk,
                "loading_broker__in":broker_params
            }
        except:
            pass
        try:
            resource_items = LoadingOrders.objects.filter(**dict2)
        except LoadingOrders.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        loading_purchase_orders ={}
        for resource_item in resource_items:
            loading_purchase_orders[resource_item.purchase_order.id]= [resource_item.quantity_loaded,resource_item.quantity+resource_item.purchase_order.pending, resource_item.quantity]
        purchase_orders = Purchaseorder.objects.filter(**dict1)
        purchase_orders_loading = Purchaseorder.objects.filter(id__in=loading_purchase_orders.keys())
        purchase_orders = (purchase_orders | purchase_orders_loading).distinct().order_by('date','id')
        purchase_orders = PurchaseorderInsideSerializer(purchase_orders, many=True).data
        for purchase_order in purchase_orders:
            try:
                loading_purchase_orders[purchase_order['id']]
                purchase_order['purchase_order'] = purchase_order['id']
                purchase_order['pending'] = loading_purchase_orders[purchase_order['id']][1]
                purchase_order['quantity_loaded'] = loading_purchase_orders[purchase_order['id']][0]
                purchase_order['quantity_per'] = loading_purchase_orders[purchase_order['id']][2]
            except:
                purchase_order['purchase_order'] = purchase_order['id']
                purchase_order['quantity_loaded'] = 0
                purchase_order['quantity_per'] = 0
        return Response(purchase_orders, status=status.HTTP_200_OK)


class GetPendingSalesOrder(APIView):

    def get(self, request, pk):
        dict1={}
        dict1['is_active']=True
        for k, v in request.query_params.items():
            fieldValue=v
            if k.endswith('__in'):
                fieldValue = request.query_params.getlist(k)
            dict1[k] = fieldValue
        try:
            party_params = dict1["party__in"]
            dict2 = {
                "is_active": True,
                "loading": pk,
                "unloading_party__in":party_params
            }
        except:
            pass
        try:
            broker_params = dict1["broker__in"]
            dict2 = {
                "is_active": True,
                "loading": pk,
                "unloading_broker__in":broker_params
            }
        except:
            pass
        try:
            resource_items = UnloadingOrders.objects.filter(**dict2)
        except LoadingOrders.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        loading_sales_orders ={}
        for resource_item in resource_items:
            loading_sales_orders[resource_item.sales_order.id]= [resource_item.quantity_unloaded,resource_item.quantity+resource_item.sales_order.pending, resource_item.quantity]
        sales_orders = SalesOrder.objects.filter(**dict1)
        sales_orders_loading = SalesOrder.objects.filter(id__in=loading_sales_orders.keys())
        sales_orders = (sales_orders | sales_orders_loading).distinct().order_by('date','id')
        sales_orders = SalesOrderInsideSerializer(sales_orders, many=True).data
        for sales_order in sales_orders:
            try:
                loading_sales_orders[sales_order['id']]
                sales_order['sales_order'] = sales_order['id']
                sales_order['pending'] = loading_sales_orders[sales_order['id']][1]
                sales_order['quantity_unloaded'] = loading_sales_orders[sales_order['id']][0]
                sales_order['quantity_per'] = loading_sales_orders[sales_order['id']][2]
            except:
                sales_order['sales_order'] = sales_order['id']
                sales_order['quantity_unloaded'] = 0
                sales_order['quantity_per'] = 0
        return Response(sales_orders, status=status.HTTP_200_OK)

class LoadingResourceView(APIView):
    """
    All the resource api will be created from here.
    """
    permission_classes = [IsAuthenticated]
    model = LoadingUnloading
    resource_serializer = LoadingSerializer
    matching_condition = 0

    def get(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoadingSerializer(resource_item)
        loading_orders = resource_item.loadingorders_set.all()
        serial = LoadingOrdersSerializer(loading_orders,many=True)
        data = {
            "loading": serializer.data,
            "loading_obj": serial.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
            loading_orders = resource_item.loadingorders_set.all()
            print(loading_orders)
            for loading_order in loading_orders:
                loading_order.delete()
            resource_item.loadingorders_set.clear()
        except:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.resource_serializer(resource_item, data=request.data['loading'], partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for loading in request.data['loading_obj']:
            loading['loading'] = serializer.data['id']
            serial = LoadingOrdersSerializer(data=loading)
            serial.is_valid(raise_exception=True)
            serial.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def put(self, request, pk):
        if pk == self.matching_condition:
            serializer = self.resource_serializer(data=request.data['loading'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            for loading in request.data['loading_obj']:
                loading['loading'] = serializer.data['id']
                serial = LoadingOrdersSerializer(data=loading)
                serial.is_valid(raise_exception=True)
                serial.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request,pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
            loading_orders = resource_item.loadingorders_set.all()
            for loading_order in loading_orders:
                loading_order.delete()
            resource_item.is_active=False
            resource_item.save()
            return Response({'message': 'The resource deleted successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class UnloadingResourceView(APIView):
    """
    All the resource api will be created from here.
    """
    permission_classes = [IsAuthenticated]
    model = LoadingUnloading
    resource_serializer = LoadingSerializer
    matching_condition = 0

    def get(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoadingSerializer(resource_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
            loading_orders = resource_item.unloading.all()
            for loading_order in loading_orders:
                loading_order.delete()
        except:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.resource_serializer(resource_item, data=request.data['unloading'], partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for loading in request.data['unloading_obj']:
            serial = UnloadingOrdersSerializer(data=loading)
            serial.is_valid(raise_exception=True)
            serial.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def put(self, request, pk):
        resource_item = self.model.objects.get(pk=pk)
        serializer = self.resource_serializer(resource_item, data=request.data['unloading'], partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for loading in request.data['unloading_obj']:
            serial = UnloadingOrdersSerializer(data=loading)
            serial.is_valid(raise_exception=True)
            serial.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request,pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
            loading_orders = resource_item.unloading.all()
            for loading_order in loading_orders:
                loading_order.delete()
            resource_item.delete()
            return Response({'message': 'The resource deleted successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class OrderDasboard(APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        s1 = SalesOrder.objects.filter(pending__gt=0,genes__startswith="paddy").values('party__name','genes','unit').annotate(Sum('pending')).order_by('party__name')
        name = s1[0]['party__name']
        new_dict = {
            name: []
        }
        for s in s1:
            if s['party__name'] == name:
                new_dict[name].append(s)
            else:
                name = s['party__name']
                new_dict[name] = [s]
        s2 = SalesOrder.objects.filter(genes__startswith="paddy").values('party__name','genes','unit').annotate(Sum('quantity'))
        name = s1[0]['party__name']
        new_dict2 = {
            name: []
        }
        for s in s2:
            if s['party__name'] == name:
                new_dict2[name].append(s)
            else:
                name = s['party__name']
                new_dict2[name] = [s]
        b = PartyBardanaBalance.objects.all()
        b = BardanaBalanceSerializer(b, many=True).data
        return Response({"pending":new_dict,"total":new_dict2, "bardana":b})


class BardanaOptionsView(APIView):
    permission_classes=[AllowAny]

    def get(self,request,pk):
        b = BillTo.objects.get(pk=pk)
        pbb = PartyBardanaBalance.objects.filter(party = b.unloaded_to)
        lst = []
        for pb in pbb:
            lst.append({
                "label":pb.quality,
                "value":pb.quality
            })
        return Response(lst)