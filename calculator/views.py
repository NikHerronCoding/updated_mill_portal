from django.shortcuts import render

from django.views import View
from .models import RecipeConcentration, RecipeName
# Create your views here.

class PricingCalculator(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'calculator/pricing_calculator.html')

class RecipeCalculator(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'calculator/recipe_calculator.html')

class DbHome(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'calculator/database_maintenance.html')

class DbSetup(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'calculator/database_create_link.html')

class DbCreation(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context = self.create_dbs()
        return render(request, 'calculator/database_create.html', context)

    def create_dbs(self):
        context = {}
        context['concentrations'] = self.create_concentrations()
        context['recipe_names'] = self.create_recipe_names()

        return context

    def create_recipe_names(self):
        self.delete_recipe_names()
        recipe_name_items = self.create_recipe_name_items()
        headers = recipe_name_items.pop(0)
        recipe_name_output = []
        for recipe_name in recipe_name_items:
            new_recipe_name = RecipeName(
                recipe_type=recipe_name[0],
                ref_number=recipe_name[1],
                rank=recipe_name[2],
                component_1=recipe_name[3],
                component_2=recipe_name[4],
                component_3=recipe_name[5],
                component_4=recipe_name[6],
                component_5=recipe_name[7],
                component_6=recipe_name[8],
                cost_component_1=recipe_name[9],
                cost_component_2=recipe_name[10],
                cost_component_3=recipe_name[11],
                cost_component_4=recipe_name[12],
                cost_component_5=recipe_name[13],
                cost_component_6=recipe_name[14],
                )
            new_recipe_name.save()
            recipe_name_output.append(new_recipe_name)

        return recipe_name_output

    def create_recipe_name_items(self):
        with open(r'/home/nherronOSM/mill_portal/calculator/recipes/recipe_names.csv') as recipe_names:
            recipe_name_rows = recipe_names.read().split('\n')
        recipe_name_items = []
        for row in recipe_name_rows:
            recipe_name_items.append(row.split(','))
        return recipe_name_items

    def delete_recipe_names(self):
        RecipeName.objects.all().delete()

    def create_concentrations(self):
        self.delete_recipe_concentrations()
        recipe_concentration_items = self.create_recipe_concentration_items()
        recipe_concentration_output = []
        headers = recipe_concentration_items.pop(0)
        for recipe_item in recipe_concentration_items:
            new_recipe = RecipeConcentration(
                recipe_type=recipe_item[0],
                concentration=recipe_item[1],
                percent_1=recipe_item[2],
                percent_2=recipe_item[3],
                percent_3=recipe_item[4],
                percent_4=recipe_item[5],
                percent_5=recipe_item[6],
                percent_6=recipe_item[7],
                )

            new_recipe.save()
            recipe_concentration_output.append(new_recipe)

        return recipe_concentration_output

    def create_recipe_concentration_items(self):
        with open(r'/home/nherronOSM/mill_portal/calculator/recipes/concentrations.csv') as recipe_concentrations:
            recipe_concentration_rows = recipe_concentrations.read().split('\n')

        recipe_concentration_items = []
        for row in recipe_concentration_rows:
            recipe_concentration_items.append(row.split(','))
        return recipe_concentration_items


    def delete_recipe_concentrations(self):
        RecipeConcentration.objects.all().delete()


