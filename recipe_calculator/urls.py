from django.urls import path
from recipe_calculator import views

app_name ='recipe_calculator'

urlpatterns = [
    path('create/', views.Create.as_view(), name='create'),
    path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
    path('update/<int:pk>', views.Update.as_view(), name='update'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
    path('list/', views.List.as_view(), name='list'),
    ]