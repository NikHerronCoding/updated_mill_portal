from django.db import models

# Create your models here.

from fabrics.models import Fabric
from brand.models import Brand
from recipe_names.models import RecipeName
from recipe_concentrations.models import RecipeConcentration

class Program(models.Model):

    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    program_recipe_name = models.ForeignKey(RecipeName, on_delete=models.CASCADE, null=True)
    program_recipe_concentration = models.ForeignKey(RecipeConcentration, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at.strftime("%m/%d/%Y")}  Program: {self.fabric.fabric_name} for {self.brand}| Recipe: {self.program_recipe_name.__str__()} {self.program_recipe_concentration.__str__()}'