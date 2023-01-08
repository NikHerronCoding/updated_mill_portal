import csv

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import Group

from recipe_names.models import RecipeName
from recipe_concentrations.models import RecipeConcentration
from django.contrib.auth.mixins import LoginRequiredMixin


class MakeRecipes(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'recipes/database_create_link.html', context)

    def post(self, request, *args, **kwargs):

        if request.user.is_staff:
            context = self.create_recipe_names_and_concentrations()
            return render(request, 'recipes/database_create.html', context)
        else:
            raise(PermissionError("You're not an Admin!!!111"))

    def create_recipe_names_and_concentrations(self):
        context = {}
        context['concentrations'] = self.create_concentrations()
        context['recipe_names'] = self.create_recipe_names()

        return context

    def create_recipe_names(self):
        recipe_name_output = []
        with open(r'/home/nherronOSM/mill_portal/recipes/recipes/recipe_names.csv') as recipe_names:
            recipe_name_rows = csv.reader(recipe_names, delimiter=',')
            next(recipe_name_rows)
            for recipe_name in recipe_name_rows:
                new_recipe_name= RecipeName(
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
                # if recipe name already exists then go ahead and update with new information
                try:
                    recipe_name = RecipeName.objects.filter(ref_number=new_recipe_name.ref_number,recipe_type= new_recipe_name.recipe_type)[0]
                    recipe_name.recipe_type = new_recipe_name.recipe_type
                    recipe_name.ref_number = new_recipe_name.ref_number
                    recipe_name.rank = new_recipe_name.rank
                    recipe_name.component_1 = new_recipe_name.component_1
                    recipe_name.component_2 = new_recipe_name.component_2
                    recipe_name.component_3 = new_recipe_name.component_3
                    recipe_name.component_4 = new_recipe_name.component_4
                    recipe_name.component_5 = new_recipe_name.component_5
                    recipe_name.component_6 = new_recipe_name.component_6
                    recipe_name.cost_component_1 = new_recipe_name.cost_component_1
                    recipe_name.cost_component_2 = new_recipe_name.cost_component_2
                    recipe_name.cost_component_3 = new_recipe_name.cost_component_3
                    recipe_name.cost_component_4 = new_recipe_name.cost_component_4
                    recipe_name.cost_component_5 = new_recipe_name.cost_component_5
                    recipe_name.cost_component_6 = new_recipe_name.cost_component_6
                    recipe_name.save()
                    new_recipe_name = recipe_name
                # if recipe name does not previously exist then save as is
                except:
                    pass
                finally:
                    new_recipe_name.save()
                    recipe_name_output.append(new_recipe_name)

        return recipe_name_output

    def create_concentrations(self):
        recipe_concentration_output = []
        with open(r'/home/nherronOSM/mill_portal/recipes/recipes/recipe_concentrations.csv') as recipe_concentrations:
            recipe_concentration_rows = csv.reader(recipe_concentrations, delimiter=',')
            next(recipe_concentration_rows)
            for recipe_concentration in recipe_concentration_rows:
                new_concentration = RecipeConcentration(
                    recipe_type=recipe_concentration[0],
                    concentration=recipe_concentration[1],
                    percent_1=recipe_concentration[2],
                    percent_2=recipe_concentration[3],
                    percent_3=recipe_concentration[4],
                    percent_4=recipe_concentration[5],
                    percent_5=recipe_concentration[6],
                    percent_6=recipe_concentration[7],
                    )

                # if recipe concentration already exists then go ahead and update with new information
                try:
                    recipe_concentration = RecipeConcentration.objects.filter(recipe_type=new_concentration.recipe_type, concentration=new_concentration.concentration)[0]
                    recipe_concentration.recipe_type = new_concentration.recipe_type
                    recipe_concentration.concentration = new_concentration.concentration
                    recipe_concentration.percent_1 = new_concentration.percent_1
                    recipe_concentration.percent_2 = new_concentration.percent_2
                    recipe_concentration.percent_3 = new_concentration.percent_3
                    recipe_concentration.percent_4 = new_concentration.percent_4
                    recipe_concentration.percent_5 = new_concentration.percent_5
                    recipe_concentration.percent_6 = new_concentration.percent_6
                    new_concentration = recipe_concentration
                #if recipe does not previously exist then save as is
                except:

                    pass
                finally:
                    new_concentration.save()
                    recipe_concentration_output.append(new_concentration)

        return recipe_concentration_output












