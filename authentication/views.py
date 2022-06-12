import datetime
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .utils import PDF, gstin
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files import File
import time
import csv
from django.http import HttpResponse
from datetime import date, datetime
from rest_framework import generics, mixins
from rest_framework import filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .serializers import RegistrationSerializer, LoginSerializer
from .renderer import UserJSONRenderer
from bills.models import BillTo, BillItem, BillBy, Expense, BillDetail
from bills.serializers import BillDetailsSerializer, ExpenseSerializer, BillDetailSerializer, BillDetailinsideSerializer, BillItemSerializer, BillSerializer,BillDetailSerializer,ForPrintingBillSerializer
from rest_framework.renderers import BaseRenderer
def getbillrowwithexpense(bill):
    billitems = bill.billitem_set.all()
    amount = 0
    bags=0 
    weight=0
    for billitem in billitems:
        amount += billitem.qty*billitem.rate
        bags += billitem.uom
        weight += billitem.qty
    expenses = bill.bill_to.expense
    if expenses:
        tulai = round(float(expenses.tulai)*amount/100,2)
        dharmada = round(float(expenses.dharmada)*amount/100,2)
        wages = round(float(expenses.wages)*weight,2)
        sutli = round(float(expenses.sutli)*bags,2)
        loading_charges = round(float(expenses.loading_charges)*bags,2)
        vikas_shulk = round(float(expenses.vikas_shulk)*amount/100,2)
        mandi_shulk = round(float(expenses.mandi_shulk)*amount/100,2)
        bardana = round(float(expenses.bardana)*bags,2)
        others = round(float(expenses.others),2)
    else:
        tulai = 0
        dharmada = 0
        wages = 0
        sutli = 0
        loading_charges = 0
        vikas_shulk = 0
        mandi_shulk = 0
        bardana = 0
        others = 0
    freight = bill.frieght
    if expenses:
        comission = round(float(expenses.commision)*amount/100,2)
    else:
        comission=0
    return {
        "bill_no" : bill.invoice_no,
        "vehicle_no": bill.vehicle_no,
        "party" : bill.bill_to.name,
        "date":bill.date,
        "bags":bags,
        "qty": weight,
        "amount":amount,
        "comission":comission,
        "tulai" :tulai,
        "dharmada":dharmada,
        "wages" :wages,
        "sutli" :sutli,
        "loading_charges" :loading_charges,
        "vikas_shulk" :vikas_shulk,
        "mandi_shulk" :mandi_shulk,
        "bardana" :bardana,
        "others" :others,
        "freight":freight,
    }
class getbillwithexpensecsv(APIView):
    def get(self,request,pk):
        Bills = BillDetail.objects.filter(bill_by=pk)
        getrows = []
        for bill in Bills:
            getrow = getbillrowwithexpense(bill)
            getrows.append(getrow)
        if getrows:
            fields_header = getrows[0].keys()
        else:
            fields_header = []
        filename = "{0}.csv".format("bill-details")
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="projects.csv"'},
        )
        writer = csv.DictWriter(response,fieldnames = fields_header)
        writer.writeheader()
        writer.writerows(getrows)
        return response
def getbillrow(bill):
    billitems = bill.billitem_set.all()
    amount = 0
    bags=0 
    weight=0
    for billitem in billitems:
        amount += billitem.qty*billitem.rate
        bags += billitem.uom
        weight += billitem.qty
    expenses = bill.bill_to.expense
    if expenses:
        act_amt = amount + round(float(expenses.tulai)*amount/100,2) + round(float(expenses.dharmada)*amount/100,2) +round(float(expenses.sutli)*bags,2) + round(float(expenses.loading_charges)*bags,2) + round(float(expenses.vikas_shulk)*amount/100,2)+ round(float(expenses.mandi_shulk)*amount/100,2) + round(float(expenses.bardana)*bags,2) + round(float(expenses.others),2)
        if bill.bill_to.id == 4:
            act_amt+=round(float(expenses.wages)*bags,2)
        else:
            act_amt+=round(float(expenses.wages)*weight,2)
    else:
        act_amt = amount
    freight = bill.frieght
    if expenses:
        comission = round(float(expenses.commision)*amount/100,2)
    else:
        comission=0
    return {
        "bill_no" : bill.invoice_no,
        "vehicle_no": bill.vehicle_no,
        "party" : bill.bill_to.name,
        "date":bill.date,
        "bags":bags,
        "qty": weight,
        "amount":amount,
        "act_amt": act_amt,
        "comission":comission,
        "freight":freight,
        "total": act_amt+comission+freight
    }
class getbillwisecsv(APIView):
    def get(self,request,pk):
        Bills = BillDetail.objects.filter(bill_by=pk)
        getrows = []
        for bill in Bills:
            getrow = getbillrow(bill)
            getrows.append(getrow)
        if getrows:
            fields_header = getrows[0].keys()
        else:
            fields_header = []
        filename = "{0}.csv".format("projects")
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="projects.csv"'},
        )
        writer = csv.DictWriter(response,fieldnames = fields_header)
        writer.writeheader()
        writer.writerows(getrows)
        return response
class getcsv(APIView):
    def get(self, request, pk):
            Bills = BillDetail.objects.filter(bill_to=pk)
            billitem = BillItem.objects.filter(bill_detail__in=Bills)
            projects = BillItemSerializer(billitem, many=True)
            projects = projects.data
            if projects:
                fields_header = projects[0].keys()
            else:
                fields_header = []
            filename = "{0}.csv".format("projects")
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="projects.csv"'},
            )
            writer = csv.DictWriter(response,fieldnames = fields_header)
            writer.writeheader()
            writer.writerows(projects)
            return response

def get_invoice(x,y):
    b = BillBy.objects.get(pk=x)
    stri = b.name.split(" ")
    strip = [ele[0] for ele in stri]
    stri = y.split("-")
    stripa= [int(ele) for ele in stri]
    if stripa[1]>3:
        year=stri[0]+"-"+str(int(stri[0])+1)
    else:
        year=str(int(stri[0])-1) + "-" + stri[0]
    try:
        bill_count = b.invoice_nos[year] +1
    except:
        bill_count = 1
    spli = "".join(strip) 
    spli = spli + "/" + year + "/"
    spli += str(bill_count).zfill(3)
    b.invoice_nos[year]=bill_count
    b.save()
    print(spli)
    return spli

def get_invoice_s(x, y,z):
    b = BillBy.objects.get(pk=x)
    stri = b.name.split(" ")
    strip = [ele[0] for ele in stri]
    stri = z.split("-")
    stripa= [int(ele) for ele in stri]
    if stripa[1]>3:
        year=stri[0]+"-"+str(int(stri[0])+1)
    else:
        year=str(int(stri[0])-1) + "-" + stri[0]
    spli = "".join(strip) 
    spli = spli + "/" + year + "/"
    spli += str(y).zfill(3)
    return spli

def get_page_pdf(pdf, biltype,billdetail):
    pdf.side_border()
    pdf.mandi_in_internal_border()
    pdf.company_name(billdetail['bill_bys'])
    pdf.set_bill_type(biltype)
    pdf.set_date_vehicle(billdetail['invoice_no'], billdetail['date'], billdetail['vehicle_no'])
    pdf.set_detail(billdetail['bill_tos'],billdetail['bill_tos']['ship_details'])
    pdf.bill_items(billdetail['billitems'])
    pdf.remarks(billdetail['remarks'])
    if billdetail['bill_to'] ==4:
        pdf.expense(bags=billdetail['total_uom'], weight=billdetail['total_uom'], expenses=billdetail['expenses'])
    else:
        pdf.expense(bags=billdetail['total_uom'], weight=billdetail['total_qty'], expenses=billdetail['expenses'])
    pdf.final_fun(billdetail['frieght'])
    pdf.total_s(billdetail['total_qty'],billdetail['total_uom'])

def gen_pdf(billdetail):
    pdf = PDF()
    get_page_pdf(pdf, 'Original',billdetail)
    get_page_pdf(pdf, 'Duplicate',billdetail)
    get_page_pdf(pdf, 'Triplicate',billdetail)
    pdf.output('invoices.pdf','F')
    return pdf

class Bill(APIView):
    def get(self, request, pk):
        billdetail = BillDetail.objects.get(pk=pk)
        billdetail = ForPrintingBillSerializer(billdetail).data
        pdf = gen_pdf(dict(billdetail))
        bill=BillDetail.objects.get(pk=pk)
        local_file = open('invoices.pdf', 'rb')
        bill.invoice.save('{}.pdf'.format("invoice"), File(local_file))
        serialize = BillDetailsSerializer(bill)
        return Response(serialize.data)

class ResourceAPIView(APIView):
    """
    All the resource api will be created from here.
    """
    permission_classes = [AllowAny]
    model = User
    resource_serializer = UserSerializer
    matching_condition = 0

    def get(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.resource_serializer(resource_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.resource_serializer(resource_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        if pk == self.matching_condition:
            serializer = self.resource_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                resource_item = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return Response({'message': 'The resource does not exist'},status=status.HTTP_400_BAD_REQUEST)
            serializer = self.resource_serializer(resource_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'},status=status.HTTP_400_BAD_REQUEST)
        resource_item.delete()
        return Response({'message': 'The resource is deleted successfully!'}, status=status.HTTP_201_CREATED)

class SetPagination(PageNumberPagination):

    page_size = 50
    page_size_query_param = 'count'

    def get_paginated_response(self, data):
        return Response(data, status=status.HTTP_200_OK)

class GetListView(generics.ListAPIView):
    model = User
    resource_serializer = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    filter_query = []
    filter_data = None
    search_fields = []
    search_fields_bill = []
    _exclude = None
    search_term = None
    search_year = None
    search_bill = None
    Q1 = Q
    special_filter = []

    def get_queryset(self, page):
        """
        queryset of the Get
        """
        if page == 'all':
            queryset = self.model.objects.all()
            for val in self.filter_query:
                queryset.filter(**val)
            if self.filter_data:
                queryset = queryset.filter(**self.filter_data)
            if self._exclude:
                queryset = queryset.exclude(**self._exclude)
            if self.search_year:
                queryset = self.get_search_results_own(
                    queryset, self.search_year)
        else:
            queryset = self.model.objects.all()
            for val in self.filter_query:
                queryset.filter(**val)
            if self.filter_data:
                queryset = queryset.filter(**self.filter_data)
            if self._exclude:
                queryset = queryset.exclude(**self._exclude)
            if self.search_term:
                queryset = self.get_search_results_own(
                    queryset, self.search_term,0)
            if self.search_year:
                queryset = self.get_search_results_own(
                    queryset, self.search_year,0)
            if self.search_bill:
                queryset = self.get_search_results_own(
                    queryset, self.search_bill,1)
        return queryset

    def list(self, request, page, *args, **kwargs):
        self.search_term = None
        self.search_year=None
        dict1 = {}
        self._exclude = {}
        self._current_special_filter = {}
        for k, v in request.query_params.items():
            fieldValue = v
            try:
                fieldValue = int(v)
            except:
                pass
            if k in self.special_filter:
                self._current_special_filter[k] = fieldValue
                continue
            if k =="search_term":
                self.search_term=v
            if k == "search_year":
                self.search_year = v
                continue
            if k == "search_bill":
                self.search_bill = v
                continue
            elif k.endswith("__exclude"):
                self._exclude[k[:-9]] = fieldValue
                continue
            if k.endswith('__in'):
                fieldValue = request.query_params.getlist(k)
            if k.endswith('__date'):
                fieldValue = datetime.datetime.strptime(fieldValue, "%Y-%m-%d")
                dict1[k[:-6]] = fieldValue
                continue
            dict1[k] = fieldValue
        if(request.GET.get('page', None) is not None):
            del dict1['page']
        if(request.GET.get('count', None) is not None):
            del dict1['count']
        if(request.GET.get('limit', None) is not None):
            del dict1['limit']
        if(request.GET.get('offset', None) is not None):
            del dict1['offset']
        if(request.GET.get('search_term', None) is not None):
            del dict1['search_term']
        self.filter_data = dict1
        queryset = self.get_queryset(page)
        if page == 'all':
            serializer = self.resource_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        page_detail = self.paginate_queryset(queryset)
        serializer = self.resource_serializer(page_detail, many=True)
        response = self.get_paginated_response(serializer.data)
        return response


    def get_search_results_own(self, queryset, search_term, a):
        if search_term == None:
            return queryset
        if len(search_term) == 0:
            return queryset
        search_queries = None
        if a:
            search_fields = self.search_fields_bill
        else:
            search_fields = self.search_fields
        for index, val in enumerate(search_fields):
            temp_field = val
            if not val.endswith("contains"):
                temp_field = "{0}__icontains".format(val)
            temp = dict()
            temp[temp_field] = search_term
            if index == 0:
                search_queries = self.Q1(**temp)
            else:
                search_queries |= self.Q1(**temp)
        if search_queries is not None:
            return queryset.filter(search_queries)
        return queryset

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        user_in = User.objects.get(id=user['id'])
        user_in.set_password(user['password'])
        user_in.save()
        return Response({"success": True}, status=status.HTTP_201_CREATED)

class GetDataUpdated(APIView):
    permission_classes=(AllowAny,)
    def get(self,request):
        bills = BillDetail.objects.all()
        for bill in bills:
            billitems = bill.billitem_set.all()
            y=[]
            for billitem in billitems:
                x = {
                    "item": billitem.item,
                    "qty":billitem.qty,
                    "uom": billitem.uom,
                    "rate":billitem.rate,
                    'po_number':billitem.po_number
                }
                y.append(x)
            bill.billitems = y
            bill.save() 
        return Response("done")

class BillResourceAPIView(APIView):
    """
    All the resource api will be created from here.
    """
    permission_classes = [AllowAny]
    model = BillDetail
    resource_serializer = BillDetailsSerializer
    matching_condition = 0

    def get(self, request, pk):
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BillDetailSerializer(resource_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        request.data['date'] = request.data['date'][:10]
        try:
            resource_item = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.resource_serializer(resource_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        if pk == self.matching_condition:
            request.data['date'] = request.data['date'][:10]
            if request.data['bw'] == "A":
                inv = get_invoice(request.data['bill_by'],request.data['date'])
                request.data['invoice_no'] = inv
            else:
                inv = get_invoice_s(request.data['bill_by'],request.data['invoice_no'],request.data['date'])
                request.data['invoice_no'] = inv
            request.data['expenses'] = BillTo.objects.get(pk=request.data['bill_to']).expense
            serializer = self.resource_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        try:
            resource_item = BillDetail.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'},status=status.HTTP_400_BAD_REQUEST)
        last_bill = BillDetail.objects.filter(bill_by=resource_item.bill_by, bw="A").last()
        if last_bill.id == resource_item.id:
            billby = BillBy.objects.get(pk=resource_item.bill_by.id)
            date = resource_item.date
            if date.month>3:
                year=str(date.year) + "-" + str(date.year+1)
            else:
                year=str(date.year-1) + "-" + str(date.year)
            billby.invoice_nos[year]=billby.invoice_nos[year]-1
            billby.save()
            resource_item.delete()
            return Response({'message': 'The resource is deleted successfully!'}, status=status.HTTP_201_CREATED)
        else:
            resource_item.is_active = False
            resource_item.save()
            return Response({"status":"updated successfully"})
