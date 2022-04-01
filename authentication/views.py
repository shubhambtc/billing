import datetime
from django.db import models
from rest_framework import status, permissions
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
    gstdetail = billdetail['gstdetail']
    if gstdetail:
        pass
    else:
        pass
    pdf.side_border()
    pdf.mandi_in_internal_border()
    pdf.company_name(billdetail['bill_by'])
    pdf.set_bill_type(biltype)
    pdf.set_date_vehicle(billdetail['invoice_no'], billdetail['date'], billdetail['vehicle_no'])
    pdf.set_detail(billdetail['bill_to'],billdetail['shipto'])
    pdf.bill_items(billdetail['bill_items'])
    pdf.remarks(billdetail['remarks'])
    if billdetail['bill_to']['id'] ==4:
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

def check_cgst_sgst(gstin1, gstin2):
    return gstin1[:2]==gstin2[:2]

def get_gstin(data):
    cgst = 0
    igst = 0
    sgst = 0
    taxable_value=0
    flag = check_cgst_sgst(data['bill_by']['gstin'],data['bill_to']['gstin'])
    for billitem in data['bill_items']:
        try:
            percent = gstin[billitem['item']]
            taxable_value += round(billitem['qty']*billitem['rate'],2)
            if flag:
                cgst += round(percent/2*billitem['qty']*billitem['rate']/100,2)
                sgst += round(percent/2*billitem['qty']*billitem['rate']/100,2)
            else:
                igst +=round(percent*billitem['qty']*billitem['rate']/100,2)
        except:
            pass
    gstin1 = {
        "cgst":cgst,
        "sgst":sgst,
        "igst":igst,
        "taxable_value":taxable_value
    }
    return gstin1

class Bill(APIView):
    def get(self, request, pk):
        billdetail = BillDetail.objects.get(pk=pk)
        billdetail = BillDetailSerializer(billdetail).data
        pdf = gen_pdf(dict(billdetail))
        bill=BillDetail.objects.get(pk=pk)
        local_file = open('invoices.pdf', 'rb')
        bill.invoice.save('{}.pdf'.format("invoice"), File(local_file))
        serialize = BillDetailSerializer(bill)
        return Response(serialize.data)

def get_expenses(b):
    if b.expense:
        expense = b.expense
        expenses = dict(ExpenseSerializer(expense).data)
    else:
        expenses = {
            'tulai':0,
            'dharmada':0,
            'wages':0,
            'mandi_shulk':0,
            'sutli':0,
            'commision':0,
            'loading_charges':0,
            'vikas_shulk':0,
            'others':0,
            'bardana':0,
        }
    return expenses

def shiptocopy(bill_to):
    return {
        "name": bill_to.name,
        "gstin": bill_to.gstin,
        "address": bill_to.address,
        "state": bill_to.state,
        "state_code": bill_to.state_code
    }

class BillInvoice(APIView):
    def put(self, request, *args, **kwargs):
        errors = {}
        serial = BillSerializer(data = request.data['bill'])
        if not serial.is_valid():
            errors.update(dict(serial.errors))
        data = request.data['billitem']
        for e in data:
            serializer = BillItemSerializer(data=e)
            if not serializer.is_valid():
                errors.update(dict(serializer.errors))
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        if request.data['bill']['bw'] == "A":
            inv = get_invoice(request.data['bill']['bill_by'],request.data['bill']['date'])
            request.data['bill']['invoice_no'] = inv
        else:
            inv = get_invoice_s(request.data['bill']['bill_by'],request.data['bill']['invoice_no'],request.data['bill']['date'])
            request.data['bill']['invoice_no'] = inv   
        bill_to = BillTo.objects.get(pk=request.data['bill']['bill_to'])
        request.data['bill']['expenses'] = get_expenses(bill_to)
        if not request.data['bill']['shipto']['name']:
            request.data['bill']['shipto'] = shiptocopy(bill_to)
        serial = BillSerializer(data = request.data['bill'])
        if serial.is_valid():
            serial.save()
            serial = serial.data
            data = request.data['billitem']
            for d in data:
                d['bill_detail'] = serial['id']
        for e in data:
            serializer = BillItemSerializer(data=e)
            if serializer.is_valid():
                serializer.save()
        billdetail = BillDetail.objects.get(pk=serial['id'])
        billdetails = BillDetail.objects.get(pk=serial['id'])
        billdetail = BillDetailSerializer(billdetail).data
        billdetails.save()
        pdf = gen_pdf(dict(billdetail))
        local_file = open('invoices.pdf', 'rb')
        billdetails.invoice.save('{}.pdf'.format("invoice"), File(local_file))
        serialize = BillDetailSerializer(billdetails)
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
        if self.model == BillTo:
            if request.data['bill_to']['bill_type'] == "MandiIn":
                if request.data['expense']['id'] == 0:
                    serial = ExpenseSerializer(data = request.data['expense'])
                    if serial.is_valid():
                        serial.save()
                        serial = serial.data
                        data = request.data['bill_to']
                        data['expense'] = serial['id']
                    else:
                        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST) 
                else:
                    # try:
                    resource = Expense.objects.get(pk=request.data['expense']['id'])
                    # except:
                        # return Response({"error":"Expense does not exists"}, status=status.HTTP_400_BAD_REQUEST)
                    serial = ExpenseSerializer(resource, data=request.data['expense'], partial=True)
                    if serial.is_valid():
                        serial.save()
                        data = request.data['bill_to']
                    else:
                        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST) 
            else:
                data = request.data['bill_to']
                data['expense'] = None
        else:
            data = request.data
        serializer = self.resource_serializer(resource_item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        if self.model == BillTo:
            if request.data['bill_to']['bill_type'] == "MandiIn":
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


class BillEdit(APIView):
    permission_classes=(AllowAny,)
    def patch(self, request,pk):
        errors = {}
        billitems =request.data['billitems']
        newbillitems =request.data['newbillitems']
        deleteitem = request.data['deletebillitem']
        try:
            resource_item = BillDetail.objects.get(pk=pk)
        except BillDetail.DoesNotExist:
            return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BillSerializer(resource_item, data=request.data['bill'], partial=True)
        if not serializer.is_valid():
            errors.update(dict(serializer.errors))
        for billitem in billitems:
            serial = BillItemSerializer(data=billitem, partial=True)
            if not serial.is_valid():
                errors.update(dict(serial.errors))
        for newbillitem in newbillitems:
            ser = BillItemSerializer(data=newbillitem)
            if not ser.is_valid():
                errors.update(dict(ser.errors))
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        for billitem in billitems:
            try:
                resource = BillItem.objects.get(pk=billitem['id'])
            except BillItem.DoesNotExist:
                return Response({'message': 'The resource does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            serial = BillItemSerializer(resource, data=billitem, partial=True)
            if serial.is_valid():
                serial.save()
        for newbillitem in newbillitems:
            newbillitem['bill_detail'] = serializer.data['id']
            ser = BillItemSerializer(data=newbillitem)
            if ser.is_valid():
                ser.save()
        BillItem.objects.filter(id__in=deleteitem).delete()
        return Response({"status":"done"})
class DeleteBill(APIView):
    permission_classes = (AllowAny,)  
    def delete(self, request,pk):
        try:
            resource_item = BillDetail.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'},status=status.HTTP_400_BAD_REQUEST)
        last_bill = BillDetail.objects.filter(bill_by=resource_item.bill_by).last()
        if last_bill.id == resource_item.id:
            billby = BillBy.objects.get(pk=resource_item.bill_by.id)
            billby.invoices_no=billby.invoices_no-1
            billby.save()
            resource_item.delete()
            return Response({'message': 'The resource is deleted successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"This bill can not be deleted"},status=status.HTTP_400_BAD_REQUEST)
class CancelBill(APIView):
    permission_classes = (AllowAny,)
    def patch(self, request,pk):
        try:
            resource_item = BillDetail.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'message': 'The resource does not exist'},status=status.HTTP_400_BAD_REQUEST)
        resource_item.is_active = False
        resource_item.save()
        return Response({"status":"updated successfully"})

class GetDataUpdated(APIView):
    permission_classes=(AllowAny,)
    def get(self,request):
        b = BillBy.objects.all()
        for a in b:
            try:
                print(a.invoice_nos["2021-2022"])
            except:
                a.invoice_nos["2021-2022"]= a.invoices_no
            a.save()
        return Response("done")
