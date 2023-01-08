import csv

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Country(models.Model):

    filepath = r'./mill_portal/static/csv_files/country_list.txt'
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=2)

    def initialize():
        with open(Country.filepath) as csvfile:
            line_count = 0
            csvreader = csv.reader(csvfile, delimiter=',')
            for line in csvreader:
                if line_count == 0:
                    pass
                else:
                    new_country = Country(name=line[0], code=line[1])
                    new_country.save()
                line_count += 1

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=32)
    country_of_origin = models.ForeignKey('Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserToBrand(models.Model):

    linked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    linked_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.linked_user} from brand: {self.linked_brand}'



