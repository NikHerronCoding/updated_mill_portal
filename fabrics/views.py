from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import inlineformset_factory
from fabrics import forms


from fabrics import models

class CreateFabric(View):
    def get(self, request,  *args, **kwargs):
        fabric_form = forms.FabricForm()
        FabricCompositionFormset = inlineformset_factory(models.Fabric, models.Fabric.compositions.through, fields=['fabric_composition' , 'percent_composition'], extra=4, can_delete=False)
        composition_formset =FabricCompositionFormset()
        context = {'fabric_form':fabric_form, 'composition_formset':composition_formset}
        return render(request, 'fabrics/fabric_create.html', context)

    def post(self, request,  *args, **kwargs):
        fabric_form = forms.FabricForm(request.POST)
        FabricCompositionFormset = inlineformset_factory(models.Fabric, models.Fabric.compositions.through, fields=['fabric_composition' , 'percent_composition'], extra=4, can_delete=False)
        if fabric_form.is_valid():
            mill_name = models.UserToMill.objects.get(linked_user=request.user).linked_mill
            fabric = fabric_form.save(commit=False)
            fabric.mill_name = mill_name
            fabric.save()

            composition_formset =FabricCompositionFormset(request.POST, instance=fabric)
            if composition_formset.is_valid():
                composition_formset.save()
                return redirect('fabrics:fabric_detail', fabric.id)
        context = {'fabric_form':fabric_form, 'composition_formset':composition_formset}
        return render(request, 'fabrics/fabric_create.html', context)

class UpdateFabric(View):
    def get(self, request, pk):
        associated_mill = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabric = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill)
        fabric_form = forms.FabricForm(instance=fabric)
        FabricCompositionFormset = inlineformset_factory(models.Fabric, models.Fabric.compositions.through, fields=['fabric_composition' , 'percent_composition'], extra=4, can_delete=True)
        composition_formset = FabricCompositionFormset(instance=fabric)
        context = {'fabric_form':fabric_form, 'composition_formset':composition_formset, 'pk':pk}
        return render(request, 'fabrics/update_fabric.html', context)

    def post(self, request, pk):
        associated_mill = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabric = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill)
        fabric_form = forms.FabricForm(request.POST, instance=fabric)
        FabricCompositionFormset = inlineformset_factory(models.Fabric, models.Fabric.compositions.through, fields=['fabric_composition' , 'percent_composition'], extra=4, can_delete=True)
        composition_formset = FabricCompositionFormset(request.POST, instance=fabric)
        if fabric_form.is_valid() and composition_formset.is_valid():
            fabric_form.save()
            composition_formset.save()
            return redirect('fabrics:fabric_detail', fabric.id)
        context = {'fabric_form':fabric_form, 'composition_formset':composition_formset, 'pk':pk}
        return render(request, 'fabrics/update_fabric.html', context)

class DetailFabric(View):
    def get(self, request, pk, *args, **kwargs):
        associated_mill = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabric_data = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill).generate_fabric_details()
        fabric = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill)
        context = {'fabric_data':fabric_data, 'fabric':fabric}
        return render(request, 'fabrics/fabric_detail.html', context)


class DeleteFabric(View):
    def get(self, request, pk):
        associated_mill = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabric = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill)
        context = {'fabric':fabric}
        return render(request, 'fabrics/confirm_delete_fabric.html', context)

    def post(self, request, pk):
        associated_mill = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabric = get_object_or_404(models.Fabric, id=pk, mill_name=associated_mill)
        fabric.delete()
        return redirect('fabrics:fabric_list')



class FabricList(View):
    def get(self, request, *args, **kwargs):
        mill_name = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabrics = models.Fabric.objects.all().filter(mill_name=mill_name).order_by('-id')[:10]
        context = {'fabrics':fabrics, 'mill_name':mill_name}
        context['fabrics_len'] = len(fabrics) < 10
        return render(request, 'fabrics/fabric_list.html', context)

class FabricListAll(View):
    def get(self, request, *args, **kwargs):
        mill_name = models.UserToMill.objects.get(linked_user=request.user).linked_mill
        fabrics = models.Fabric.objects.all().filter(mill_name=mill_name).order_by('-id')
        context = {'fabrics':fabrics, 'mill_name':mill_name}
        context['fabrics_len'] = len(fabrics) < 10
        return render(request, 'fabrics/fabric_list_all.html', context)




