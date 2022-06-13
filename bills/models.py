from email.policy import default
from django.db import models
from billsystem.storage_backends import OverwriteStorage
# Create your models here.
BILL_TYPE_CHOICES = [
    ('MandiIn','MandiIn'),
    ('MandiOut','MandiOut')
]
BILL_INFO_CHOICES = [
    ('bill_to','bill_to'),
    ('bill_to_ship_to','bill_to_ship_to')
]

class BillTo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    gstin = models.CharField(max_length=255, blank=True, null=True)
    bill_type = models.CharField(max_length=255, choices=BILL_TYPE_CHOICES)
    bill_info = models.CharField(max_length=255, choices=BILL_INFO_CHOICES, null=True,blank=True)
    ship_details = models.JSONField(default=dict,null=True,blank=True)
    party_username = models.CharField(max_length=255,null=True,blank=True)
    expense = models.JSONField(default=dict,null=True,blank=True)

class BillBy(models.Model):
    name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=255)
    mobile1 = models.CharField(max_length=10)
    mobile2 = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, default="uttar pradesh")
    state_code = models.IntegerField(blank=True, default=9)
    bank_name = models.CharField(max_length=255)
    bank_account_no = models.CharField(max_length=255)
    bank_ifsc = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    invoices_no = models.IntegerField(default=0,null=True, blank=True)
    invoice_nos = models.JSONField(default=dict)
    sign = models.ImageField(upload_to="sign", blank=True,null=True)
BW_CHOICES = [('A','A'), ('B','B')]
class BillDetail(models.Model):
    invoice_no = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    vehicle_no = models.CharField(max_length=255, blank=True, null=True)
    bill_to = models.ForeignKey(BillTo, on_delete=models.CASCADE)
    bill_by = models.ForeignKey(BillBy, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=255, default='', blank=True, null=True)
    bw = models.CharField(max_length=255, default='A', choices=BW_CHOICES)
    frieght = models.IntegerField(default=0)
    invoice = models.FileField(upload_to="invoices",default=None, blank=True, null=True, storage=OverwriteStorage())
    expenses = models.JSONField(default=dict)
    shipto = models.JSONField(default=dict)
    billitems = models.JSONField(default=list)
    gstdetail = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)