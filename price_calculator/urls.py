from django.urls import path
from price_calculator import views
app_name = 'price_calculator'
urlpatterns = [
    path('create/', views.PricingCalculatorCreate.as_view(), name='pricing_calculator_create' ),
    path('list/', views.PricingCalculatorList.as_view(), name='pricing_calculator_list'),
    path('list_all/',views.PricingCalculatorListAll.as_view(), name='pricing_calculator_list_all'),
    path('detail/<int:pk>/', views.PricingCalculatorDetail.as_view(), name='pricing_calculator_detail'),
    path('update/<int:pk>/', views.PricingCalculatorUpdate.as_view(), name='pricing_calculator_update'),
    path('delete/<int:pk>/', views.PricingCalculatorDelete.as_view(), name='pricing_calculator_delete'),
    ]