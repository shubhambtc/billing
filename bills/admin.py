from django.contrib import admin
from .models import Expense, BillTo, BillBy, BillDetail, BillItem

# Register your models here.
admin.site.register(Expense)
admin.site.register(BillTo)
admin.site.register(BillBy)
admin.site.register(BillDetail)
admin.site.register(BillItem)