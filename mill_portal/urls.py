
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView, name='osm-home'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('docs/', include('docs.urls')),
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),
    path('fabrics/', include('fabrics.urls', namespace='fabrics')),
    path('mill_procedure/', include('mill_procedure.urls', namespace='mill_procedure')),
    path('recipes/', include('recipes.urls', namespace='recipes')),
    path('test/', views.TestView.as_view(), name='osm-test'),
    path('price_calculator/', include('price_calculator.urls', namespace='price_calculator')),
    path('recipe_calculator/', include('recipe_calculator.urls', namespace='recipe_calculator')),
    path('order/', include('order.urls', namespace='order')),
]
