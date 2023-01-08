from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import os


class DocsHome(LoginRequiredMixin, View):
    login_url="/login/"
    def get(self, request, **kwargs):
        return render(request, 'docs/docs_home.html')


def stream_sds(request, chem_name, *args, **kwargs):
    file_path = f'/home/nherronOSM/mill_portal/mill_portal/static/sds/individual/{chem_name}'
    try:
        pdf_to_send = open(file_path, 'rb')
    except FileNotFoundError:
        new_file_path = f'/home/nherronOSM/mill_portal/mill_portal/static/sds/mixed/{chem_name}'
        pdf_to_send = open(new_file_path, 'rb')
    return FileResponse(pdf_to_send, as_attachment=True, filename=f'{chem_name}')



class SdsView(View, LoginRequiredMixin):
    login_url="/login/"

    def get(self, request):
        old_dir = os.getcwd()
        new_dir = '/home/nherronOSM/mill_portal/mill_portal/static/sds/'
        os.chdir(new_dir)
        files = {}
        items = []
        titles = []

        for item in os.walk('.'):
            items.append(item)
        os.chdir(old_dir)

        for idx, file in enumerate(items):
            if idx == 0:
                next
            else:
                title = file[0].replace('./', '')
                titles.append(title)
                files[title] = file[2]

        return render(request, 'docs/sds_list.html', files)

class TdsView(View, LoginRequiredMixin):
    login_url="/login/"

    def get(self, request):
        old_dir = os.getcwd()
        new_dir = '/home/nherronOSM/mill_portal/mill_portal/static/tds/'
        os.chdir(new_dir)
        files = {}
        items = []
        titles = []

        for item in os.walk('.'):
            items.append(item)
        os.chdir(old_dir)

        for idx, file in enumerate(items):
            if idx == 0:
                next
            else:
                title = file[0].replace('./', '')
                titles.append(title)
                files[title] = file[2]

        return render(request, 'docs/tds_list.html', files)

def stream_tds(request, chem_name, *args, **kwargs):
    file_path = f'/home/nherronOSM/mill_portal/mill_portal/static/tds/individual/{chem_name}'
    try:
        pdf_to_send = open(file_path, 'rb')
    except FileNotFoundError:
        new_file_path = f'/home/nherronOSM/mill_portal/mill_portal/static/tds/mixed/{chem_name}'
        pdf_to_send = open(new_file_path, 'rb')
    return FileResponse(pdf_to_send, as_attachment=True, filename=f'{chem_name}')