from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from fabrics.models import Fabric, UserToMill
from price_calculator.forms import PricingCalculatorForm
from price_calculator.models import PricingCalculator

# Create your views here.


class PricingCalculatorCreate(View):
    def get(self, request, *args, **kwargs):
        form = PricingCalculatorForm()
        mill_name = get_object_or_404(UserToMill, linked_user=request.user).linked_mill
        queryset = Fabric.objects.filter(mill_name=mill_name)
        form.fields['fabric'].queryset = queryset
        context = {'form':form}
        return render(request,'price_calculator/pricing_calculator_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PricingCalculatorForm(request.POST)
        if form.is_valid():
            pricing_calculator = form.save(commit=False)
            pricing_calculator.linked_user = request.user
            pricing_calculator.save()
            return redirect('price_calculator:pricing_calculator_detail', pricing_calculator.id)
        context = {'form':form}
        return render(request,'price_calculator/pricing_calculator_create.html', context)

class PricingCalculatorList(View):
    def get(self, request, *args, **kwargs):
        pricing_calculators = PricingCalculator.objects.filter(linked_user=request.user).order_by('-id')[:10]
        context = {'pricing_calculators':pricing_calculators}
        return render(request, 'price_calculator/pricing_calculator_list.html', context)

class PricingCalculatorListAll(View):
    def get(self, request, *args, **kwargs):
        pricing_calculators = PricingCalculator.objects.filter(linked_user=request.user).order_by('-id')
        context = {'pricing_calculators':pricing_calculators}
        return render(request, 'price_calculator/pricing_calculator_list.html', context)


class PricingCalculatorDetail(View):
    def get(self, request, pk, *args, **kwargs):
        pricing_calculator = get_object_or_404(PricingCalculator, linked_user=request.user, id=pk)
        fabric_data = pricing_calculator.fabric.generate_fabric_details()
        cost_data = pricing_calculator.cost_form_dict()
        context = {'pricing_calculator':pricing_calculator, 'fabric_data':fabric_data, 'cost_data':cost_data}
        return render(request, 'price_calculator/pricing_calculator_detail.html', context)

class PricingCalculatorUpdate(View):
    def get(self, request, pk, *args, **kwargs):
        pricing_calculator = get_object_or_404(PricingCalculator, linked_user=request.user, id=pk)
        form = PricingCalculatorForm(instance=pricing_calculator)
        context = {'form':form, 'pk':pk}
        return render(request, 'price_calculator/pricing_calculator_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        instance=get_object_or_404(PricingCalculator, id=pk, linked_user=request.user)
        form = PricingCalculatorForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=False)
            form.linked_user = request.user
            form.save()

            return redirect('price_calculator:pricing_calculator_detail', pk)
        context = {'form':form, 'messages':['form data invalid']}
        return render(request,'price_calculator/pricing_calculator_update.html', context)

class PricingCalculatorDelete(View):
    def get(self, request, pk, *args, **kwargs):
        pricing_calculator = get_object_or_404(PricingCalculator, id=pk, linked_user=request.user)
        context = {'pricing_calculator':pricing_calculator}
        return render(request, 'price_calculator/pricing_calculator_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        pricing_calculator = get_object_or_404(PricingCalculator, id=pk, linked_user=request.user)
        pricing_calculator.delete()
        return redirect('price_calculator:pricing_calculator_list')




