from django.shortcuts import render, get_object_or_404
from django.views import View
# Create your views here.

from brand.models import UserToBrand
from order.models import OrderPdf




class ListView(View):

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_to_brand = UserToBrand.objects.get(linked_user=current_user)
        brand = user_to_brand.linked_brand
        orders = OrderPdf.objects.filter(brand=brand).order_by('-date')
        name = request.user.get_full_name()
        context = {'UserToBrand':user_to_brand, 'orders':orders, 'name':name, 'brand':brand}
        return render(request, 'order/list.html', context)



class PdfStreamView(View):
    def get(self, request, pk, *args, **kwargs):
        current_user = request.user
        user_to_brand = UserToBrand.objects.get(linked_user=current_user)
        brand = user_to_brand.linked_brand
        order = get_object_or_404(OrderPdf, id=pk, brand=brand)
        return order.stream_pdf(request)
