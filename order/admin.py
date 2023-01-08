from django.contrib import admin
from order.models import Order, Carrier, OrderPdf
# Register your models here.

admin.site.register(Order)
admin.site.register(Carrier)
admin.site.register(OrderPdf)
