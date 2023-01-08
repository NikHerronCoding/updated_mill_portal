from django.forms import ModelForm
from price_calculator.models import PricingCalculator

class PricingCalculatorForm(ModelForm):

    class Meta:
        model=PricingCalculator
        fields = ['fabric',
                'auto_generate_recipe',
                'recipe_name',
                'recipe_concentration']
