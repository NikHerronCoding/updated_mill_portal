from django.urls import path
from mill_procedure import views

app_name ='mill_procedure'

urlpatterns = [
    path('create/', views.MillProcedureCreate.as_view(), name='mill_procedure_create'),
    path('update/<int:pk>', views.MillProcedureUpdate.as_view(), name='mill_procedure_update'),
    path('delete/<int:pk>', views.MillProcedureDelete.as_view(), name='mill_procedure_delete'),
    path('detail/<int:pk>', views.MillProcedureDetail.as_view(), name='mill_procedure_detail'),
    path('spreadsheet/<int:pk>', views.MillProcedureGenerateSpreadsheet.as_view(), name='mill_procedure_spreadsheet'),
    path('list/', views.MillProcedureList.as_view(), name='mill_procedure_list'),
    path('test/', views.MillProcedureTest.as_view(), name='test'),
    ]