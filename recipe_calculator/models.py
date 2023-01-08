# standard library imports
from math import isclose

# django library imports
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


# project imports
from fabrics.models import Fabric, CompositionsInFabric
from recipe_names.models import RecipeName
from recipe_concentrations.models import RecipeConcentration


class RecipeCalculator(models.Model):

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


    CHEMISTRY_TYPE_CHOICES = [
        ("EVO", "EVO (non-fluorinated)"),
        ("NORR", "NORR (fluorinated)"),
        ]

    #   default recommended recipes curated by OSM staff
    #   NORR
    DEFAULT_RECOMMENDED_SYNTHETIC_RECIPE_NORR = RecipeName.objects.get(recipe_type="NORR", ref_number="027-003" )
    DEFAULT_RECOMMENDED_CELLULOSIC_RECIPE_NORR = RecipeName.objects.get(recipe_type="NORR", ref_number="048-049" )
    DEFAULT_RECOMMENDED_LOW_TEMP_RECIPE_NORR = RecipeName.objects.get(recipe_type="NORR", ref_number="043-003" )
    #   EVO
    DEFAULT_RECOMMENDED_SYNTHETIC_RECIPE_EVO = RecipeName.objects.get(recipe_type="EVO", ref_number="025-003" )
    DEFAULT_RECOMMENDED_CELLULOSIC_RECIPE_EVO = RecipeName.objects.get(recipe_type="EVO", ref_number="025-003" )
    DEFAULT_RECOMMENDED_LOW_TEMP_RECIPE_EVO = RecipeName.objects.get(recipe_type="EVO", ref_number="032-003" )


    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    chemistry_type = models.CharField(max_length=8, choices=CHEMISTRY_TYPE_CHOICES)

    finishing_temperature = models.IntegerField()
    finishing_speed = models.IntegerField()
    tenter_frame_length = models.IntegerField()


    linked_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'''{self.created_at.strftime('%d-%m-%Y')} | Fabric: {self.fabric.fabric_name} | Recipe: {self.calculate_recipe_name() } {self.calculate_recipe_concentration()} | {round(self.tenter_frame_length * 60 / self.finishing_speed) } seconds at {self.finishing_temperature}°C  '''

    def calculate_recipe_name(self):
        if self.calculate_percent_synthetic() >= 65 and self.finishing_temperature >= 140:
            if self.chemistry_type == 'NORR':
                return self.DEFAULT_RECOMMENDED_SYNTHETIC_RECIPE_NORR
            else:
                return self.DEFAULT_RECOMMENDED_SYNTHETIC_RECIPE_EVO
        elif self.calculate_percent_synthetic() <= 65 and self.finishing_temperature >= 140:
            if self.chemistry_type == 'NORR':
                return self.DEFAULT_RECOMMENDED_CELLULOSIC_RECIPE_NORR
            else:
                return self.DEFAULT_RECOMMENDED_CELLULOSIC_RECIPE_EVO
        else:
            if self.chemistry_type == 'NORR':
                return self.DEFAULT_RECOMMENDED_LOW_TEMP_RECIPE_NORR
            else:
                return self.DEFAULT_RECOMMENDED_LOW_TEMP_RECIPE_EVO

    #    function calculated the total concentration of DWR to use to the nearest .25
    def calculate_recipe_concentration(self):
        percent_concentration =  round((self.calculate_base_recipe_concentration() * self.calculate_recipe_concentration_multiplier()) * 4) / 4
        concentrations = RecipeConcentration.objects.all().filter(recipe_type="MV")
        for concentration in concentrations:
            if  isclose(concentration.percent_1, percent_concentration):
                return concentration

        return concentrations.filter(percent_1 = 5.0)


    #   returns the base recipe concentration to use (the minimum that could ever be used in the calculator reliably) Norr = 1.5%, EVO = 2.5%
    def calculate_base_recipe_concentration(self):
        if self.chemistry_type == 'NORR':
            return 1.5
        else:
            return 2.5


    #   function determines what total concentration should be above baseline numbers. works for NORR and EVO
    def calculate_recipe_concentration_multiplier(self):

        if self.fabric.fabric_construction in ["KS", "WF"] and self.calculate_percent_synthetic() >= 90 and self.calculate_percent_nylon() <= 85:
            return 1.0
        elif self.fabric.fabric_construction in ["KS", "WF"] and self.calculate_percent_synthetic() >= 35:
            return 1.66666667
        elif self.fabric.fabric_construction in ["KS", "WF"] and self.calculate_percent_synthetic() <= 35:
            return 2.5
        elif self.fabric.fabric_construction in ["KB","WB", "U"] and self.calculate_percent_synthetic() >= 90:
            return 1.66666667
        elif self.fabric.fabric_construction in ["KB","WB", "U"] and self.calculate_percent_synthetic() >= 35:
            return 2.5
        elif self.fabric.fabric_construction in ["KB","WB", "U"] and self.calculate_percent_synthetic() <= 35:
            return 3.33333333
        else:
            return 1.6666667

    #    Calculates the percent synthetic fiber content in the textile
    def calculate_percent_synthetic(self):
        percent_synthetic = 0
        compositions = CompositionsInFabric.objects.filter(fabric=self.fabric)
        for composition in compositions:
            if composition.fabric_composition.composition in self.SYNTHETIC_COMPOSITIONS:
                percent_synthetic += composition.percent_composition
        return percent_synthetic

    def calculate_percent_nylon(self):
        percent_nylon = 0
        compositions = CompositionsInFabric.objects.filter(fabric=self.fabric)
        for composition in compositions:
            if composition.fabric_composition.composition == 'Nylon':
                percent_nylon += composition.percent_composition
        return percent_nylon

    #   Calculates the percent cellulosic fiber content in the textile
    def calculate_percent_cellulosic(self):
        percent_cellulosic = 0
        compositions = CompositionsInFabric.objects.filter(fabric=self.fabric)
        for composition in compositions:
            if composition.fabric_composition.composition in self.CELLULOSIC_CHOICES:
                percent_cellulosic += composition.percent_composition
        return percent_cellulosic


    def generate_results(self):
        return {'cure_temp': str(self.finishing_temperature) + ' °C', 'cure_time':str(round(self.tenter_frame_length* 60 / self.finishing_speed )) + ' Seconds', 'recipe_name':self.calculate_recipe_name(), 'recipe_concentration':self.calculate_recipe_concentration()}








