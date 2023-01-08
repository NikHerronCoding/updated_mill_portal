from django.db import models

from recipe_names.models import RecipeName
from program.models import Program
from supplier.models import Supplier
from fabrics.models import Mill
from brand.models import Brand

from django.http import FileResponse


# Create your models here.

class Order(models.Model):

    shipping_type_choices = [('Air Freight', 'Air Freight'), ('Sea Freight', 'Sea Freight'), ('Train Freight', 'Train Freight'), ('Truck Freight', 'Truck Freight') ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    mill = models.ForeignKey(Mill, on_delete=models.CASCADE )
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_type = models.CharField(max_length=64, choices=shipping_type_choices,null=True)
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE, null=True)
    chemistry_type = models.ForeignKey( RecipeName, on_delete=models.CASCADE,null=True)
    amount = models.FloatField(null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    identifier = models.CharField(max_length=8, null=True)

class Carrier(models.Model):
    name = models.CharField(max_length=64)
    tracking_page = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'



class OrderPdf(models.Model):
    date = models.DateTimeField()
    order_number = models.CharField(max_length=16, null=True)
    order_pdf = models.FileField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    def stream_pdf(self, request, *args, **kwargs):
        file_path = self.order_pdf.path
        try:
            pdf_to_send = open(file_path, 'rb')
        except:
            pass
        return FileResponse(pdf_to_send, as_attachment=True, filename=f'{self.order_number}.pdf')



