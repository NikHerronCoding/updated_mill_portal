#  django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

#  project imports
from recipe_calculator.models import RecipeCalculator
from recipe_calculator.forms import RecipeCalculatorForm
from fabrics.models import UserToMill, Fabric


# Create your views here.


class Create(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        mill_name = UserToMill.objects.get(linked_user=request.user).linked_mill
        form = RecipeCalculatorForm()
        form.fields['fabric'].queryset = Fabric.objects.filter(mill_name=mill_name)
        return render(request, 'recipe_calculator/create.html', {'form':form})
    def post(self, request, *args, **kwargs):
        form = RecipeCalculatorForm(request.POST)
        if form.is_valid():
            recipe_calculator = form.save(commit=False)
            recipe_calculator.linked_user = request.user
            recipe_calculator.save()

            return redirect('recipe_calculator:detail', recipe_calculator.id)
        else:
            return render(request, 'recipe_calculator/create.html', {'form':form})

class Detail(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        recipe_calculator = get_object_or_404(RecipeCalculator, linked_user=request.user, id=pk)
        fabric_data = recipe_calculator.fabric.generate_fabric_details()
        recipe_parameters = recipe_calculator.generate_results()
        return render(request, 'recipe_calculator/detail.html', {'recipe_calculator':recipe_calculator, 'fabric_data':fabric_data, 'recipe_results':recipe_parameters})

class Update(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        mill_name = UserToMill.objects.get(linked_user=request.user).linked_mill
        recipe_calculator = get_object_or_404(RecipeCalculator, linked_user=request.user, id=pk)
        form = RecipeCalculatorForm(instance=recipe_calculator)
        form.fields['fabric'].queryset = Fabric.objects.filter(mill_name=mill_name)
        return render(request, 'recipe_calculator/update.html', {'form':form})


    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(RecipeCalculator, id=pk, linked_user=request.user)
        form = RecipeCalculatorForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=False)
            form.linked_user = request.user
            form.save()
            return redirect('recipe_calculator:detail', pk)
        context = {'form':form, 'messages':['form data invalid']}
        return render(request,'recipe_calculator/update.html', context)


class Delete(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        recipe_calculator = get_object_or_404(RecipeCalculator, id=pk, linked_user=request.user)
        context = {'recipe_calculator':recipe_calculator}
        return render(request, 'recipe_calculator/confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        recipe_calculator = get_object_or_404(RecipeCalculator, id=pk, linked_user=request.user)
        recipe_calculator.delete()
        return redirect('recipe_calculator:list')


class List(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        recipe_calculator_context = []
        recipe_calculator_list = RecipeCalculator.objects.filter(linked_user=request.user).order_by('-id')
        for recipe_calculator in recipe_calculator_list:
            full_recipe = recipe_calculator.generate_results()['recipe_name'].__str__() +' ' + recipe_calculator.generate_results()['recipe_concentration'].__str__()
            cure_specs = recipe_calculator.generate_results()['cure_temp'] + ' '+ recipe_calculator.generate_results()['cure_time']
            output_recipe_context = {'recipe_calculator':recipe_calculator, 'recipe':full_recipe, 'cure_specs':cure_specs}
            recipe_calculator_context.append(output_recipe_context)

        context = {'recipe_calculator_context':recipe_calculator_context}
        return render(request, 'recipe_calculator/list.html', context)
