from django.db import models

# Create your models here.
CHOICE = [('in','IN'),('out','OUT')]
UNIT_CHOICE = [('50_kg_bag','50 kg Bag'),('60_kg_bag','60 kg Bag')]
class Party(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Warehouse(models.Model):
    party = models.ForeignKey(Party,on_delete=models.CASCADE)
    date = models.DateField()
    in_or_out = models.CharField(choices=CHOICE,max_length=255)
    qty = models.IntegerField()
    unit = models.CharField(choices=UNIT_CHOICE,max_length=255)
    loading_charges = models.IntegerField(default=0)

    def __str__(self):
        return self.party.name + " | " + str(self.date) + " | " + self.in_or_out