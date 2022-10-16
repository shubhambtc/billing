from django.db import models
from requests import delete
from yaml import BlockMappingStartToken
# Create your models here.

PARTY_TYPE_CHOICE = [
    ('bilty','bilty'),
    ('sales','sales'),
    ('purchase','purchase'),
    ('mandi-purchase','mandi-purchase'),
    ('mandi-sales','mandi-sales'),
    ('broker','broker'),
]

class OrderParty(models.Model):
    party_type = models.CharField(choices=PARTY_TYPE_CHOICE,max_length=255,null=True,blank=True,default='both')
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    brokerage = models.FloatField(null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)



class SalesOrder(models.Model):
    sales_type = models.CharField(max_length=255)
    party = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="salesparty")
    broker = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="salesbroker")
    date = models.DateField(null=True,blank=True)
    genes = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.FloatField(null=True,blank=True)
    unit = models.CharField(max_length=255,null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    condition = models.CharField(max_length=255,null=True,blank=True)
    po_number = models.CharField(max_length=255,null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    pending = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pending = self.quantity
        super(SalesOrder, self).save(*args, **kwargs)


class Purchaseorder(models.Model):
    purchase_type = models.CharField(max_length=255)
    party = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="purchaseparty")
    broker = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="purchasebroker")
    date = models.DateField()
    genes = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.FloatField(null=True,blank=True)
    unit = models.CharField(max_length=255,null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    condition = models.CharField(max_length=255,null=True,blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    pending = models.FloatField(null=True,blank=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            self.pending = self.quantity
        super(Purchaseorder, self).save(*args, **kwargs)


class LoadingUnloading(models.Model):
    loading_from = models.ManyToManyField(OrderParty, related_name="loading_party")
    date = models.DateField()
    genes = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=255,null=True, blank=True)
    quantity = models.FloatField()
    freight = models.FloatField(null=True,blank=True)
    frieght_paid_at_loading = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    bill_or_builty = models.CharField(max_length=255,null=True,blank=True)
    unloaded = models.BooleanField(default=False)
    unloaded_to = models.ManyToManyField(OrderParty, related_name="unloaded_party", blank=True)
    unloading_date=models.DateField(null=True,blank=True)
    unloaded_quantity = models.FloatField(null=True, blank=True)
    frieght_at_unloading = models.FloatField(null=True,blank=True)
    unloading_remarks = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=True)


class LoadingOrders(models.Model):
    loading_party = models.ForeignKey(OrderParty, on_delete=models.CASCADE, null=True, blank=True, related_name="party")
    loading_broker = models.ForeignKey(OrderParty, on_delete=models.CASCADE, null=True, blank=True, related_name="broker")
    loading = models.ForeignKey(LoadingUnloading, null=True, blank=True, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(Purchaseorder, null=True,blank=True, on_delete=models.CASCADE)
    quantity_loaded = models.FloatField(null=True,blank=True)
    quantity = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        print(self.pk)
        if not self.pk:
            self.purchase_order.pending -= self.quantity
            self.purchase_order.save()
        super(LoadingOrders, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.purchase_order.pending+=self.quantity
        self.purchase_order.save()
        self.is_active=False
        super(LoadingOrders, self).delete(*args,**kwargs)

class UnloadingOrders(models.Model):
    unloading_party = models.ForeignKey(OrderParty, on_delete=models.CASCADE, null=True, blank=True, related_name="unloading_party")
    unloading_broker = models.ForeignKey(OrderParty, on_delete=models.CASCADE, null=True, blank=True, related_name="unloading_broker")
    loading = models.ForeignKey(LoadingUnloading, null=True, blank=True, on_delete=models.CASCADE, related_name="unloading")
    sales_order = models.ForeignKey(SalesOrder, null=True,blank=True, on_delete=models.CASCADE)
    quantity_unloaded = models.FloatField(null=True,blank=True)
    quantity = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            self.sales_order.pending -= self.quantity
            self.sales_order.save()
        super(UnloadingOrders, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.sales_order.pending+=self.quantity
        self.sales_order.save()
        self.is_active=False
        super(UnloadingOrders, self).delete(*args,**kwargs)


class PartyBardanaBalance(models.Model):
    party = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="bardanabalaceparty")
    quantity = models.IntegerField(default=0)
    quality = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class BardanaInward(models.Model):
    party = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="bardanainparty")
    quantity = models.IntegerField()
    freight_amount = models.FloatField()
    vehicle_no = models.CharField(max_length=255)
    date = models.DateField()
    quality = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            print(self)
            b = PartyBardanaBalance.objects.get_or_create(party=self.party, quality=self.quality)
            print(b[0].quantity)
            print(self.quantity)
            b[0].quantity+=int(self.quantity)
            b[0].save()
        super(BardanaInward, self).save(*args, **kwargs)

class BardanaOutward(models.Model):
    party = models.ForeignKey(OrderParty, on_delete=models.CASCADE,null=True,blank=True, related_name="bardanaoutarty")
    quantity = models.IntegerField()
    bill_no = models.CharField(max_length=255)
    vehicle_no = models.CharField(max_length=255)
    quality = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            b = PartyBardanaBalance.objects.get_or_create(party=self.party, quality=self.quality)
            b[0].quantity-=int(self.quantity)
            b[0].save()
        super(BardanaOutward, self).save(*args, **kwargs)