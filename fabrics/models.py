from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User

from brand.models import Country


class Address(models.Model):
    street_address_1 = models.CharField(max_length=64)
    street_address_2 = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=32)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.street_address_1}, {self.street_address_2} \n{self.city} {self.state}, {self.zip_code}, \n{self.country}'


class Fabric(models.Model):


    FABRIC_WEIGHT_UNIT_CHOICES = [('OZYD', 'oz/yd^2 (Ounces per square yard)'),('GSM','g/m^2 (GSM)')]
    FABRIC_WIDTH_UNIT_CHOICES = [('IN', 'Inches (in)'),('CM','Centimeters (cm)')]
    FABRIC_CONSTRUCTION_CHOICES = [
        ("KS", "Knit - Smooth / Filament"),
        ("KB", "Knit - Brushed / Fleeced / Hairy"),
        ("WF", "Woven-Flat"),
        ("WB", "Woven-Brushed / Fleeced / Decorative / Hairy"),
        ("U", "Upholstery"),
        ]

    FABRIC_CONSTRUCTIONS = {
            "KS":"Knit - Smooth / Filament",
            "KB":"Knit - Brushed / Fleeced / Hairy",
            "WF":"Woven-Flat",
            "WB":"Woven-Brushed / Fleeced / Decorative / Hairy",
            "U":"Upholstery",
            }
    END_USE_CHOICES = [
        ("A", "Apparel",),
        ("U", "Upholstery"),
        ("M", "Medical"),
        ("I", "Industrial"),]

    END_USES = {"A":'Apparel',
                "U":'Upholstery',
                "M":'Medical',
                "I":'Industrial'}

    FABRIC_COMPOSITION_CHOICES = [
        ("S", "Synthetic: Polyester, Nylon, Spandex, Acrylic or Polyolefin"),
        ("C", "Cellulosic: Cotton, Linen, Flax, Bamboo, Rayon, Acetate ETC"),
        ("A", "Animal: Wool, Cashmere, Alpaca"),]


    end_customer = models.CharField(max_length=32)
    mill_name = models.ForeignKey('Mill', on_delete=models.CASCADE)
    fabric_name = models.CharField(max_length=32)
    fabric_weight = models.FloatField()
    fabric_weight_unit = models.CharField(max_length=8, choices=FABRIC_WEIGHT_UNIT_CHOICES, default='GSM')
    fabric_width = models.FloatField()
    fabric_width_unit = models.CharField(max_length=16, choices=FABRIC_WIDTH_UNIT_CHOICES, default='IN')
    end_use = models.CharField(max_length=32, choices=END_USE_CHOICES)
    fabric_construction = models.CharField(max_length=8, choices=FABRIC_CONSTRUCTION_CHOICES)

    compositions = models.ManyToManyField('FabricComposition', through='CompositionsInFabric',related_name="fabrics_composition")


    def composition_valid(self):
        composition_sum = 0
        compositions = CompositionsInFabric.objects.all().filter(fabric=self)

        for composition in compositions:
            composition_sum += composition.percent_composition
        if composition_sum == 100:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.fabric_name} for {self.end_customer}"

    def generate_fabric_details(self):
        fabric_details = OrderedDict()
        fabric_details['fabric_name'] = self.fabric_name
        fabric_details['mill_name'] = self.mill_name
        fabric_details['end_customer'] = self.end_customer
        fabric_details['fabric_weight'] = self.fabric_weight
        fabric_details['fabric_weight_unit'] = self.fabric_weight_unit
        fabric_details['fabric_width'] = self.fabric_width
        fabric_details['fabric_width_unit'] = self.fabric_width_unit
        fabric_details['end_use'] = self.END_USES[self.end_use]
        fabric_details['fabric_construction'] = self.FABRIC_CONSTRUCTIONS[self.fabric_construction],
        fabric_details['compositions'] = self.get_compositions()
        return fabric_details

    def get_compositions(self):
        output = []
        compositions = CompositionsInFabric.objects.filter(fabric=self)
        for composition in compositions:
            output.append([composition.percent_composition, composition.fabric_composition.composition])
        return output



class FabricComposition(models.Model):



    SYNTHETIC_COMPOSITIONS = [
        'Polyester',
        'Nylon',
        'Spandex',
        'Acrylic',
        'Polyolefin',
        'Sorona (PBT)',
        ]

    CELLULOSIC_CHOICES = [
        'Cotton',
        'Linen',
        'Flax',
        'Bamboo',
        'Rayon',
        'Acetate',
        ]

    ANIMAL_COMPOSITIONS = [
        'Wool',
        'Cashmere',
        'Alpaca',
        ]

    NONE = [
        'Unknown'
        ]

    FABRIC_COMPOSITION_CHOICES = [(item, item) for item in (SYNTHETIC_COMPOSITIONS + CELLULOSIC_CHOICES + ANIMAL_COMPOSITIONS + NONE)]

    composition = models.CharField(max_length=64, choices=FABRIC_COMPOSITION_CHOICES, default='Unknown')

    def __str__(self):
        return self.composition



class CompositionsInFabric(models.Model):
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    fabric_composition = models.ForeignKey(FabricComposition, on_delete=models.CASCADE)
    percent_composition = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.fabric.fabric_name} contains {self.percent_composition}% {self.fabric_composition.composition[:10]}"

class Mill(models.Model):
    mill_name = models.CharField(max_length=32)
    mill_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    linked_user = models.ManyToManyField(User, through='UserToMill', related_name='mill_users')

    def __str__(self):
        return self.mill_name


class UserToMill(models.Model):
    linked_mill = models.ForeignKey(Mill, on_delete=models.CASCADE)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.linked_user.username} from {self.linked_mill.mill_name}'




























