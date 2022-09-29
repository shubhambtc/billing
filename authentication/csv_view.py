from typing import List
import csv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import BaseParser
from rest_framework.views import APIView
from authentication.serializers import *
from bills.models import BillBy, BillDetail, BillTo
from rest_framework.permissions import AllowAny
class CSVTextParser(BaseParser):

    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None) -> List[List]:
        charset = 'utf-8'
        media_type_params = dict([param.strip().split('=')
                                 for param in media_type.split(';')[1:]])
        charset = media_type_params.get('charset', 'latin1')
        dialect = media_type_params.get('dialect', 'excel')
        txt = stream.read().decode(charset)
        csv_table = list(csv.DictReader(txt.splitlines(), dialect=dialect))
        return csv_table

class BillDetailCSV(APIView):
    parser_classes = (CSVTextParser,)
    permission_classes = [AllowAny]
    def put(self, request):
        content_type = request.content_type.split(';')[0].strip()
        encoding = 'utf-8'
        if content_type == 'text/csv':
            csv_table = request.data
            response = {}
            response['not_added'] = []
            count =0
            for row in csv_table:
                billitem = [{
                    "uom" : row['uom'],
                    "item": row['item'],
                    "qty": row['qty'],
                    "net_qty": row['net_qty'],
                    "rate":row['rate'],
                    "po_number": ""
                }]
                bill_by = BillBy.objects.get(pk=row['bill_by'])
                bill_to = BillTo.objects.get(pk=row['bill_to'])
                e = BillDetail.objects.create(
                    invoice_no =row['invoice_no'],
                    date =row['date'],
                    vehicle_no =row['vehicle_no'],
                    bill_to =bill_to,
                    bill_by =bill_by,
                    bw =row['bw'],
                    frieght =row['advance'],
                    expenses =bill_to.expense,
                    billitems =billitem,
                    bilty_type =row['bilty'],
                    frieght_per_qtl =row['freight_per_qtl']
                )
                count = count +1
            response['count'] = count
            response['success'] = "Successfully Uploaded"
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unsupported Media Type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)