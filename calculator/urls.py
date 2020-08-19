from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('recipe_calculator/', views.RecipeCalculator.as_view(), name='recipe_calculator'),
    path('pricing_calculator/', views.PricingCalculator.as_view(), name='pricing_calculator'),
    path('database_maintenance/', views.DbHome.as_view(), name='db-home'),
    path('database_create_link/', views.DbSetup.as_view(), name='db-create-link'),
    path('database_create/', views.DbCreation.as_view(), name='db-create')
    ]

