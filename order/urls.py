from django.urls import path
from order import views
app_name = 'order'
urlpatterns = [
    path('list/', views.ListView.as_view(), name='pdf-orders' ),
    path('pdf_stream/<int:pk>', views.PdfStreamView.as_view(), name='pdf-stream'),

    ]