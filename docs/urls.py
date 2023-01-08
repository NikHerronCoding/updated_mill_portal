from django.urls import path
from . import views

app_name = 'docs'


urlpatterns = [
    path('', views.DocsHome.as_view(), name="docs_home"),
    path('sds', views.SdsView.as_view(), name='sds_list'),
    path('sds/<str:chem_name>', views.stream_sds, name = 'sds_stream'),
    path('sds/<str:chem_name>', views.stream_sds, name = 'sds_stream'),
    path('tds', views.TdsView.as_view(), name='tds_list'),
    path('tds/<str:chem_name>', views.stream_tds, name = 'tds_stream'),
    path('tds/<str:chem_name>', views.stream_tds, name = 'tds_stream'),
    ]
