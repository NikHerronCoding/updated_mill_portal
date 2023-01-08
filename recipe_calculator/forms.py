#  django imports
from django.forms import ModelForm

#  project imports
from recipe_calculator.models import RecipeCalculator


class RecipeCalculatorForm(ModelForm):

    class Meta:
        model = RecipeCalculator

        fields = ['fabric',
                  'chemistry_type',
                  'finishing_temperature',
                  'finishing_speed',
                  'tenter_frame_length',]

        labels = {
                'finishing_temperature':'Finishing Temperature (°C)',
                'finishing_speed':'Finishing Speeed (Meters/Min)',
                'tenter_frame_length':'Tenter Frame Length (Meters)',
        }

