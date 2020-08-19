from django.urls import path
from . import views

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('calculator/', include('calculator.urls')),
    path('admin/', admin.site.urls),
    path('', views.HomePageView)
]
