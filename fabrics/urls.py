from django.urls import path
from fabrics import views
app_name = 'fabrics'
urlpatterns = [
    path('create/', views.CreateFabric.as_view(), name='fabric_create' ),
    path('update/<int:pk>/', views.UpdateFabric.as_view(), name='fabric_update'),
    path('detail/<int:pk>/', views.DetailFabric.as_view(), name='fabric_detail'),
    path('list/', views.FabricList.as_view(), name='fabric_list'),
    path('list_all/', views.FabricListAll.as_view(), name='fabric_list_all'),
    path('delete/<int:pk>', views.DeleteFabric.as_view(), name='fabric_delete'),
    ]