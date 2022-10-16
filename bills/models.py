from email.policy import default
from django.db import models
from billsystem.storage_backends import OverwriteStorage
from ckeditor.fields import RichTextField
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
    from orders.models import OrderParty
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
    unloaded_to = models.ForeignKey(OrderParty, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Bilty(models.Model):
    name=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    mob=models.CharField(max_length=255,blank=True,null=True)
    gstin=models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    types = models.IntegerField(null=True, blank=True)
    nos = models.JSONField(default=dict)
class BillBy(models.Model):
    from orders.models import OrderParty
    name = models.CharField(max_length=255)
    shortname=models.CharField(max_length=255, null=True,blank=True)
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
    invoice_nos = models.JSONField(default=dict)
    sign = models.ImageField(upload_to="sign", blank=True,null=True)
    is_active = models.BooleanField(default=True)
    loading_from = models.ForeignKey(OrderParty, null=True, blank=True,on_delete=models.CASCADE)
    bilty=models.ForeignKey(Bilty,null=True,blank=True, on_delete=models.CASCADE)
    bilty_add = models.CharField(null=True, blank=True, max_length=100)
    types = models.CharField(default="mandi_in",max_length=255)

BW_CHOICES = [('A','A'), ('B','B')]
BT_CHOICES = [('to_pay','To Pay'), ('for','F. O. R')]

class BillDetail(models.Model):
    invoice_no = models.CharField(max_length=255, blank=True, null=True)
    bilty_no = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    vehicle_no = models.CharField(max_length=255, blank=True, null=True)
    bill_to = models.ForeignKey(BillTo, on_delete=models.CASCADE)
    bill_by = models.ForeignKey(BillBy, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=255, default='', blank=True, null=True)
    bw = models.CharField(max_length=255, default='A', choices=BW_CHOICES)
    frieght = models.IntegerField(default=0)
    invoice = models.FileField(upload_to="invoices",default=None, blank=True, null=True, storage=OverwriteStorage())
    expenses = models.JSONField(default=dict)
    billitems = models.JSONField(default=list)
    bardana_details = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    nine_r = models.CharField(max_length=255,blank=True,null=True)
    gatepass = models.CharField(max_length=255, blank=True, null=True)
    bilty_type = models.CharField(max_length=255, default='to_pay', choices=BT_CHOICES,null=True,blank=True)
    frieght_per_qtl = models.IntegerField(null=True,blank=True)

class LetterHead(models.Model):
    party=models.ForeignKey(BillBy, on_delete=models.CASCADE)
    matter = RichTextField()
