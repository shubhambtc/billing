from django.db import models

# Create your models here.

PARTY_TYPE_CHOICE = [
    ('sale','sale'),
    ('purchase','purchase'),
    ('both','both')
]

class OrderParty(models.Model):
    party_type = models.CharField(choices=PARTY_TYPE_CHOICE,max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

class Broker(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    brokerage = models.FloatField(null=True,blank=True)



