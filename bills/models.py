from django.db import models
from billsystem.storage_backends import OverwriteStorage
# Create your models here.
BILL_TYPE_CHOICES = [
    ('MandiIn','MandiIn'),
    ('MandiOut','MandiOut')
]
class Expense(models.Model):
    tulai = models.FloatField(null=True, blank=True)
    dharmada = models.FloatField(null=True, blank=True)
    wages = models.FloatField(null=True, blank=True)
    mandi_shulk = models.FloatField(null=True, blank=True)
    sutli = models.FloatField(null=True, blank=True)
    commision = models.FloatField(null=True, blank=True)
    loading_charges = models.FloatField(null=True, blank=True)
    vikas_shulk = models.FloatField(null=True, blank=True)
    others = models.FloatField(null=True, blank=True)
    bardana = models.FloatField(null=True, blank=True)

class BillTo(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    gstin = models.CharField(max_length=255)
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
BW_CHOICES = [('A','A'), ('B','B')]
class BillDetail(models.Model):
    invoice_no = models.CharField(max_length=255)
    date = models.DateField()
    vehicle_no = models.CharField(max_length=255)
    bill_to = models.ForeignKey(BillTo, on_delete=models.CASCADE, blank=True, null=True)
    bill_by = models.ForeignKey(BillBy, on_delete=models.CASCADE, blank=True, null=True)
    remarks = models.CharField(max_length=255, default='', blank=True, null=True)
    bw = models.CharField(max_length=255, default='A', choices=BW_CHOICES)
    frieght = models.IntegerField(default=0)
    invoice = models.FileField(upload_to="invoices",default=None, blank=True, null=True, storage=OverwriteStorage())

class BillItem(models.Model):
    bill_detail = models.ForeignKey(BillDetail, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    rate = models.IntegerField()
    qty = models.FloatField()
    uom = models.IntegerField(blank=True, default=100)
    po_number = models.CharField(max_length=255, default="")