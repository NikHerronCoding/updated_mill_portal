import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from fabrics.models import Fabric
from recipe_names.models import RecipeName
from recipe_concentrations.models import RecipeConcentration

class MillProcedure(models.Model):

    # generating the default choices for the fields below
    cure_specs_known_choices = [(True, 'Yes, I will enter it below'),(False, 'No, I will assume that the default values below are ok.')]
    run_length_unit_choices = [('YD','yards(Yds)'),('M','meters(m)')]

    yards_to_meters = 0.9144
    inches_to_meters = 0.0254
    ozyd_to_gsm = 33.9057
    gram_to_kilogram = 0.001
    percent_to_ratio = 0.01


    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    run_length = models.IntegerField(default=100000)
    run_length_unit = models.CharField(max_length=4, choices=run_length_unit_choices, default='YD')
    wet_pick_up_percent = models.FloatField(default=60.0)
    curing_specs_known = models.BooleanField(choices=cure_specs_known_choices, default=False)
    cure_temp = models.IntegerField(default=170)
    cure_time = models.IntegerField(default=120)
    mixing_tank_size = models.FloatField(default=100)
    recipe_name = models.ForeignKey(RecipeName, on_delete=models.CASCADE)
    recipe_concentration = models.ForeignKey(RecipeConcentration, on_delete=models.CASCADE)
    linked_user = models.ForeignKey(User,on_delete=models.CASCADE, default = 1, related_name='user_to_mill_procedure')
    create_date = models.DateField(default=timezone.now)


    def __str__(self):
        return f" {self.create_date} | Fabric {self.fabric} | {self.fabric.end_customer} | {self.fabric.mill_name} | Recipe: {self.recipe_name.__str__()} {self.recipe_concentration.__str__()}"

    # returns total cost of the chemistry per kg taking into account the ratios of each component and the cost of each
    def recipe_cost_per_kg(self):
        component_1_cost = (self.recipe_concentration.percent_1 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_1
        component_2_cost = (self.recipe_concentration.percent_2 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_2
        component_3_cost = (self.recipe_concentration.percent_3 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_3
        component_4_cost = (self.recipe_concentration.percent_4 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_4
        component_5_cost = (self.recipe_concentration.percent_5 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_5
        component_6_cost = (self.recipe_concentration.percent_6 / self.recipe_concentration.percent_total()) * self.recipe_name.cost_component_6

        return (component_1_cost + component_2_cost + component_3_cost + component_4_cost + component_5_cost + component_6_cost)


    # returns length of fabric run in meters regardless of input unit
    def get_meter_length(self):
        if self.run_length_unit =='M':
            return self.run_length
        else:
            return self.run_length * self.yards_to_meters
    #  return widths of the fabric in meters regardless of input unit
    def get_meter_width(self):
        if self.fabric.fabric_width_unit == 'CM':
            return self.fabric.fabric_width * 0.01
        else:
            return self.fabric.fabric_width * self.inches_to_meters
    # returns total square meters of fabric treated IE width * length in meters
    def total_square_meters(self):
      return self.get_meter_width() * self.get_meter_length()

    # returns the fabric weight in terms of GSM regardless on input unit
    def get_fabric_gsm(self):
        if self.fabric.fabric_weight_unit == 'GSM':
            return self.fabric.fabric_weight
        else:
            return self.fabric.fabric_weight * self.ozyd_to_gsm

    # returns total fabric weight in kilograms**
    def total_fabric_weight(self):
        return round(self.total_square_meters() * self.get_fabric_gsm() * self.gram_to_kilogram, 2)

    # # NOT USED AT THE MOMENT returns total chemical usage from minimum bath requirements
    # def min_bath_chemical_usage(self):
    #   return round(( self.minimum_bath * self.recipe_concentration.percent_total * self.percent_to_ratio / (self.wet_pick_up_percent * self.percent_to_ratio)),2)

    #  returns strictly the chemistry used just to treat the fabric and nothing else
    def fabric_chemical_usage(self):
        return round(self.recipe_concentration.percent_total() * self.percent_to_ratio * self.total_fabric_weight(), 2)


    # returns the total chemical usage in KG for a production run
    def total_chemical_usage(self):
        return round(self.fabric_chemical_usage() + self.min_bath_chemical_usage(),2)

    def calculate_chemical_mixing_amount(self):
        return round((self.recipe_concentration.percent_total() * self.mixing_tank_size / self.wet_pick_up_percent),2)


    def create_data_form(self):

        output_dict= {
            "end_customer":self.fabric.end_customer,
            "mill_name":self.fabric.mill_name.__str__(),
            "fabric_weight":self.fabric.fabric_weight,
            "fabric_name":self.fabric.fabric_name,
            "fabric_weight_unit":self.fabric.fabric_weight_unit,
            "fabric_width":self.fabric.fabric_width,
            "fabric_width_unit":self.fabric.fabric_width_unit,
            "run_length":self.run_length,
            "run_length_unit":self.run_length_unit,
            "wet_pick_up_percent":self.wet_pick_up_percent,
            "cure_temp": self.cure_temp,
            "cure_time":self.cure_time,
            "mixing_tank_size":self.mixing_tank_size,
            "recipe_name": self.recipe_name.__str__(),
            "recipe_concentration":self.recipe_concentration.__str__()}
        return output_dict

    # returns calculated mixing amounts and structures the data in a format that is compaible with the form object for this class
    def calculate_mixing_amounts(self):
        mixing_amounts = {
                'mixing_tank_size':round(self.mixing_tank_size, 1),
                'chemical_name':f"{self.recipe_name.__str__()} {self.recipe_concentration.__str__()}",
                'amount_chemical':self.calculate_chemical_mixing_amount(),
                'amount_water':(self.mixing_tank_size - self.calculate_chemical_mixing_amount()),
            }
        return mixing_amounts

    def generate_cells(self):
        # getting all needed data from the mill_procedure object model
        customer_name = self.fabric.mill_name.__str__()
        fabric_name = self.fabric.fabric_name
        full_recipe = self.recipe_name.__str__() + " " + self.recipe_concentration.__str__()
        chemical_name = self.recipe_name.__str__() + " " + self.recipe_concentration.recipe_type
        cure_temp = str(self.cure_temp) + ' C'
        cure_time = str(self.cure_time) + ' Seconds'
        wet_pick_up = self.wet_pick_up_percent
        bath_size = self.mixing_tank_size
        default_chemical_usage = round(self.recipe_concentration.percent_total() * self.mixing_tank_size / 100, 2)
        default_water_usage = self.mixing_tank_size - default_chemical_usage
        if wet_pick_up == 100.0:
            specific_wet_pick_up = "Wet Pick Up Same as Default"
            specific_chemical_usage = "Same Amount as Default"
            specific_water_usage = "Same Amount as Default"

        else:
            specific_wet_pick_up = wet_pick_up
            specific_chemical_usage = round(default_chemical_usage / (specific_wet_pick_up / 100), 2)
            specific_water_usage = bath_size - specific_chemical_usage

        # mapping aquired data from the model to cells in the desired spreadsheet
        output_cells = {}
        output_cells['B9'] = customer_name
        output_cells['B10'] = fabric_name
        output_cells['B11'] = full_recipe
        output_cells['B14'] = chemical_name
        output_cells['B19'] = cure_temp
        output_cells['B20'] = cure_time
        output_cells['C14'] = default_chemical_usage
        output_cells['C16'] = bath_size
        output_cells['C17'] = default_water_usage
        output_cells['E15'] = chemical_name
        output_cells['F14'] = (specific_wet_pick_up /100 if type(specific_wet_pick_up) == type(4.0) else specific_wet_pick_up )
        output_cells['F15'] = specific_chemical_usage
        output_cells['F16'] = bath_size
        output_cells['F17'] = specific_water_usage
        output_cells['I6'] = datetime.datetime.today().strftime('%d-%b-%Y')

        return output_cells

