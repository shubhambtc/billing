from email.policy import default
from django.db import models
from billsystem.storage_backends import OverwriteStorage
from jsonfield import JSONField
# Create your models here.
BILL_TYPE_CHOICES = [
    ('MandiIn','MandiIn'),
    ('MandiOut','MandiOut')
]


class Expense(models.Model):
    tulai = models.FloatField(null=True, blank=True, default=0)
    dharmada = models.FloatField(null=True, blank=True, default=0)
    wages = models.FloatField(null=True, blank=True, default=0)
    mandi_shulk = models.FloatField(null=True, blank=True, default=0)
    sutli = models.FloatField(null=True, blank=True, default=0)
    commision = models.FloatField(null=True, blank=True, default=0)
    loading_charges = models.FloatField(null=True, blank=True, default=0)
    vikas_shulk = models.FloatField(null=True, blank=True, default=0)
    others = models.FloatField(null=True, blank=True, default=0)
    bardana = models.FloatField(null=True, blank=True, default=0)

class BillTo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    gstin = models.CharField(max_length=255, blank=True, null=True)
    bill_type = models.CharField(max_length=255, choices=BILL_TYPE_CHOICES)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)

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
    
    gstdetail = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

class BillItem(models.Model):
    bill_detail = models.ForeignKey(BillDetail, on_delete=models.CASCADE, blank=True, null=True)
    item = models.CharField(max_length=255)
    rate = models.FloatField()
    qty = models.FloatField()
    uom = models.IntegerField(blank=True, default=100)
    po_number = models.CharField(max_length=255, default="", blank=True)

class Dara(models.Model):
    bill_to = models.ForeignKey(BillTo,on_delete=models.CASCADE)
    purchase_date = models.DateField(default="2021-01-01")
    loading_date = models.DateField(default="2021-01-01")
    vehicle_no = models.CharField(max_length=255, default="", blank=True)
    dara = models.JSONField(default=list, blank=True, null=True)
    weight = models.FloatField()
    rate = models.FloatField()