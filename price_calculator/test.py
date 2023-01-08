from .models import PricingCalculator

def get_obj():
    return PricingCalculator.objects.all()[0]