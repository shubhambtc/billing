from django.contrib import admin
from .models import BillTo, BillBy, BillDetail, LetterHead

# Register your models here.
admin.site.register(BillTo)
admin.site.register(BillBy)
admin.site.register(BillDetail)
admin.site.register(LetterHead)