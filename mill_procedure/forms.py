from django.forms import ModelForm
from mill_procedure.models import MillProcedure


class MillProcedureForm(ModelForm):

    class Meta:
        model=MillProcedure
        fields = ['fabric',
                'run_length',
                'run_length_unit',
                'wet_pick_up_percent',
                'curing_specs_known',
                'cure_temp',
                'cure_time',
                'mixing_tank_size',
                'recipe_name',
                'recipe_concentration']

        labels = {
            "end_customer":"End Customer",
            "mill_name":"Mill Name",
            "fabric_weight":"Fabric Weight",
            "fabric_name":"Fabric Name",
            "fabric_weight_unit":"Fabric Weight Unit",
            "fabric_width":"Fabric Width",
            "fabric_width_unit":"Fabric Width Unit",
            "run_length":"Run Length",
            "wet_pick_up_percent":"Wet Pickup - If left alone we will guess 60%",
            "cure_temp": "Cure Temp (Celsius)",
            "cure_time":"Cure Time (seconds)",
            "mixing_tank_size":"Mixing Tank Size (kg)",
            "recipe_name": "Recipe Name",
            "recipe_concentration":"Recipe Concentration",
        }
