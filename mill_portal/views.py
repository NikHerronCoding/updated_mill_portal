from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


def HomePageView(request):
    return render(request, 'home.html')

class TestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'test.html')

class ContactUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contact_us.html')


