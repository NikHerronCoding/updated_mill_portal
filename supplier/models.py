from django.db import models

from fabrics.models import Address

# Create your models here.

class Supplier(models.Model):

    name = models.CharField(max_length=64)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'Supplier: {self.name}'

