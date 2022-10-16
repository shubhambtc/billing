from django.contrib import admin
from .models import OrderParty, SalesOrder, Purchaseorder, LoadingUnloading, LoadingOrders, UnloadingOrders, PartyBardanaBalance,BardanaInward,BardanaOutward
# Register your models here.

admin.site.register(OrderParty)
admin.site.register(SalesOrder)
admin.site.register(Purchaseorder)
admin.site.register(LoadingUnloading)
admin.site.register(LoadingOrders)
admin.site.register(UnloadingOrders)
admin.site.register(PartyBardanaBalance)
admin.site.register(BardanaOutward)
admin.site.register(BardanaInward)
