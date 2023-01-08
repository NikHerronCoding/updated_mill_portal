from django import forms
from fabrics.models import Fabric, CompositionsInFabric

class FabricForm(forms.ModelForm):

    class Meta:
        model=Fabric
        fields = ['end_customer',
                    'fabric_name',
                    'fabric_weight',
                    'fabric_weight_unit',
                    'fabric_width',
                    'fabric_width_unit',
                    'end_use',
                    'fabric_construction', ]




class CompositionsInFabricForm(forms.ModelForm):

    class Meta:
        model = CompositionsInFabric
        fields = ['fabric_composition', 'percent_composition']
