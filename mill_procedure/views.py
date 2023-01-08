#standard library imports
from tempfile import NamedTemporaryFile

#django imports
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

#appliction imports
from fabrics.models import Fabric, UserToMill
from mill_procedure.forms import MillProcedureForm
from mill_procedure.models import MillProcedure

#third party imports
import openpyxl

class MillProcedureTest(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mill_procedure/mill_procedure_create_test.html')


class MillProcedureCreate(View):
    def get(self, request, *args, **kwargs):
        context = {}
        mill_name = get_object_or_404(UserToMill, linked_user=request.user).linked_mill
        mill_procedure_form = MillProcedureForm()
        mill_procedure_form.fields['fabric'].queryset = Fabric.objects.filter(mill_name=mill_name)
        context['mill_procedure_form'] = mill_procedure_form
        return render(request, 'mill_procedure/create.html', context)

    def post(self, request, *args, **kwargs):
        mill_procedure_form = MillProcedureForm(request.POST)
        if mill_procedure_form.is_valid():
            mill_procedure = mill_procedure_form.save(commit=False)
            mill_procedure.linked_user = request.user
            mill_procedure.save()
            return redirect('mill_procedure:mill_procedure_detail', mill_procedure.id)
        else:
            context = {'mill_procedure_form':mill_procedure_form}
            return render(request, 'mill_procedure/create.html', context)

class MillProcedureUpdate(View):
    def get(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, linked_user=request.user, id=pk)
        mill_procedure_form = MillProcedureForm(instance=mill_procedure)
        context = {'form':mill_procedure_form, 'pk':pk}
        return render(request, 'mill_procedure/mill_procedure_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, linked_user=request.user, id=pk)
        mill_procedure_form = MillProcedureForm(request.POST, instance=mill_procedure)
        if mill_procedure_form.is_valid():
            new_mill_procedure = mill_procedure_form.save(commit=False)
            new_mill_procedure.save()
            return redirect('mill_procedure:mill_procedure_detail', pk)

class MillProcedureDelete(View):
    def get(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, id=pk, linked_user=request.user)
        context = {'mill_procedure':mill_procedure}
        return render(request, 'mill_procedure/mill_procedure_confirm_delete.html', context)
    def post(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, id=pk, linked_user=request.user)
        mill_procedure.delete()
        return redirect('mill_procedure:mill_procedure_list')

class MillProcedureDetail(View):
    def get(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, linked_user=request.user, id=pk)
        mill_procedure_data = mill_procedure.create_data_form()
        mixing_amounts = mill_procedure.calculate_mixing_amounts()
        fabric_data = mill_procedure.fabric.generate_fabric_details()
        context = {'mill_procedure_data':mill_procedure_data, 'mixing_amounts':mixing_amounts, 'fabric_data':fabric_data, 'mill_procedure':mill_procedure}
        return render(request, 'mill_procedure/mill_procedure_details.html', context)

class MillProcedureGenerateSpreadsheet(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, id=pk, linked_user=request.user)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename=Mill Procedure {mill_procedure.fabric.fabric_name}.xlsx'
        xlsx_data = self.make_spreadsheet(request, pk)
        response.write(xlsx_data)
        return response

    def make_spreadsheet(self, request, pk, *args, **kwargs):
        mill_procedure = get_object_or_404(MillProcedure, id=pk, linked_user=request.user)
        cells_to_update = mill_procedure.generate_cells()
        workbook =  openpyxl.load_workbook('/home/nherronOSM/mill_portal/mill_portal/static/spreadsheet templates/Mill Procedure Template.xlsx')

        for cell in cells_to_update:
            workbook['Mill Procedure'][cell].value = cells_to_update[cell]

        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()

        return stream

class MillProcedureList(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        queryset = MillProcedure.objects.filter(linked_user=user).order_by('-id')
        context['queryset_len'] = len(queryset) < 10
        context['mill_procedures'] = queryset
        return render(request, 'mill_procedure/list.html', context)


