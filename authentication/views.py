import datetime
from django.db import models
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .utils import PDF
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files import File
import time
from datetime import date
from rest_framework import generics, mixins
from rest_framework import filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .serializers import RegistrationSerializer, LoginSerializer
from .renderer import UserJSONRenderer
from bills.models import BillTo, BillItem, BillBy, Expense, BillDetail
from bills.serializers import ExpenseSerializer, BillDetailSerializer, BillDetailinsideSerializer, BillItemSerializer, BillSerializer
from rest_framework.renderers import BaseRenderer

def get_invoice(x):
    b = BillBy.objects.get(pk=x)
    stri = b.name.split(" ")
    strip = [ele[0] for ele in stri]
    bill_count = b.invoices_no +1
    spli = "".join(strip) 
    spli = spli + "/2021-2022/"
    spli += str(bill_count).zfill(3)
    b.invoices_no=bill_count
    b.save()
    return spli

    
def get_page_pdf(pdf, biltype,pk):
    bill = BillDetail.objects.get(pk=pk)
    bi = bill.billitem_set.all()
    bit = bill.billitem_set.aggregate(Sum('qty'),Sum('uom'))
    pdf.side_border()
    pdf.mandi_in_internal_border()
    pdf.company_name(bill.bill_by)
    pdf.set_bill_type(biltype)
    pdf.set_date_vehicle(bill.invoice_no, bill.date.strftime("%d %b %Y "), bill.vehicle_no)
    pdf.set_detail(bill.bill_to)
    pdf.bill_items(bi)
    pdf.remarks(bill.remarks)
    pdf.expense(bags=bit['uom__sum'], weight=bit['qty__sum'], expenses=bill.bill_to.expense)
    pdf.final_fun(bill.frieght)
    pdf.total_s(bit['qty__sum'],bit['uom__sum'])

def gen_pdf(pk):
    pdf = PDF()
    get_page_pdf(pdf, 'Original',pk)
    get_page_pdf(pdf, 'Duplicate',pk)
    get_page_pdf(pdf, 'Triplicate',pk)
    pdf.output('invoices.pdf','F')
    return pdf

def current_user_details(request):
    user = User.objects.get(email=request.user.email)
    if user.current_organisation_id is None:
        raise ValueError("User must have a current organisation id")
    return dict(
        user=user,
        user_id=user.id,
        organisation_id=user.current_organisation_id_id
    )

def attach_to_dict(data, current_info, model):
    """
    Attaching current info to dict

    Args:
        data (object): data model object
        current_info (dict): value we need to set
    """
    organisation_key = "organisation_id"
    if issubclass(model, models.Model):
        for key, val in data.items():
            if key == "form":
                continue
            if key == "current_organisation_id":
                data[key] = current_info["user"].current_organisation_id_id
            attach_current_info(val, current_info, model)
        organisation_key = "auth_organisation_id"
    if "id" not in data or data["id"] == 0 or data["id"] == "" or data["id"] is None:
        data["created_on"] = current_info["created_on"]
        data["created_by"] = current_info["user_id"]
        data[organisation_key] = current_info["organisation_id"]
    data["modified_on"] = current_info["created_on"]
    data["modified_by"] = current_info["user_id"]

def attach_to_list(data, current_info, model):
    for val in data:
        attach_to_dict(val, current_info, model)

def attach_current_info(data, current_info, model):
    if isinstance(data, dict):
        attach_to_dict(data, current_info, model)
    elif isinstance(data, list):
        attach_to_list(data, current_info, model)
class Bill(APIView):
    def get(self, request, pk):
        # try:
            gen_pdf(pk)
            bill=BillDetail.objects.get(pk=pk)
            local_file = open('invoices.pdf', 'rb')
            bill.invoice.save('{}.pdf'.format("invoice"), File(local_file))
            serialize = BillDetailSerializer(bill)
            return Response(serialize.data)
        # except:
        #     return Response({'status':"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class BillInvoice(APIView):
    def put(self, request, *args, **kwargs):
        inv = get_invoice(request.data['bill']['bill_by'])
        request.data['bill']['invoice_no'] = inv
        serial = BillSerializer(data = request.data['bill'])
        if serial.is_valid():
            serial.save()
            serial = serial.data
            data = request.data['billitem']
            for d in data:
                d['bill_detail'] = serial['id']
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        for e in data:
            serializer = BillItemSerializer(data=e)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pdf = gen_pdf(serial['id'])
        bill=BillDetail.objects.get(pk=serial['id'])
        local_file = open('invoices.pdf', 'rb')
        bill.invoice.save('{}.pdf'.format("invoice"), File(local_file))
        serialize = BillDetailSerializer(bill)
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
        if self.model == BillTo:
            if request.data['bill_to']['bill_type'] == "MandiIn":
                print("1")
                serial = ExpenseSerializer(data = request.data['expense'])
                if serial.is_valid():
                    serial.save()
                    serial = serial.data
                    data = request.data['bill_to']
                    data['expense'] = serial['id']
                else:
                    return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST) 
            else:
                data = request.data['bill_to']
                data['expense'] = None
            
        else:
            data = request.data
        if pk == self.matching_condition:
            serializer = self.resource_serializer(data=data)
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
    pagination_class = SetPagination
    filter_backends = [filters.SearchFilter]
    filter_query = []
    filter_data = None
    search_fields = []
    _exclude = None
    search_term = None
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
            if self.search_term:
                queryset = self.get_search_results_own(
                    queryset, self.search_term)
        else:
            m = int(page)
            if m == 0 or m == 1:
                queryset = self.model.objects.all()
                for val in self.filter_query:
                    queryset.filter(**val)
                if self.filter_data:
                    queryset = queryset.filter(**self.filter_data)
                if self._exclude:
                    queryset = queryset.exclude(**self._exclude)
                if self.search_term:
                    queryset = self.get_search_results_own(
                        queryset, self.search_term)
                queryset = queryset[:50]
            else:
                n = (m-1)*50
                queryset = self.model.objects.all()[n:n+50]
                for val in self.filter_query:
                    queryset.filter(**val)
                if self.filter_data:
                    queryset = queryset.filter(**self.filter_data)
                if self._exclude:
                    queryset = queryset.exclude(**self._exclude)
                if self.search_term:
                    queryset = self.get_search_results_own(
                        queryset, self.search_term)
                queryset = queryset[n:n+50]
        return queryset

    def list(self, request, page, *args, **kwargs):
        self.search_term = None
        page_count = request.GET.get('page', None)
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
            if k == "search":
                self.search_term = v
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
        self.filter_data = dict1
        queryset = self.get_queryset(page)
        serializer = self.resource_serializer(queryset, many=True)
        if page == 'all':
            length = len(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        page_detail = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page_detail)


    def get_search_results_own(self, queryset, search_term):
        if search_term == None:
            return queryset
        if len(search_term) == 0:
            return queryset
        search_queries = None
        for index, val in enumerate(self.search_fields):
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


