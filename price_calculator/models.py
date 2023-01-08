#django imports
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#project imports
from recipe_names.models import RecipeName
from recipe_concentrations.models import RecipeConcentration
from fabrics.models import Fabric


class PricingCalculator(models.Model):

    LIST_PRICES = {'NORR': 195.0,
                    'EVO': 160.0}

    #  unit options for the database
    fabric_weight_unit_choices = [('OZYD', 'oz/yd^2 (Ounces per square yard)'),('GSM','g/m^2 (GSM)')]
    fabric_width_unit_choices = [('IN', 'Inches (in)'),('CM','Centimeters (cm)')]
    price_output_unit_choices = [('USD', 'American Dollars ($USD)'), ('RMB', 'Chinese Yuan (RMB)')]
    run_length_unit_choices = [('YD','yards(Yds)'),('M','meters(m)')]

    #  unit conversions
    ozyd_to_gsm = 33.9057
    yards_to_meters = 0.9144
    inches_to_meters = 0.0254
    gram_to_kilogram = 0.001
    kilogram_to_gram = 1000
    percent_to_ratio = 0.01
    kg_to_lb = 2.20462


    #  fields
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    recipe_name = models.ForeignKey(RecipeName, on_delete=models.CASCADE)
    recipe_concentration = models.ForeignKey(RecipeConcentration, on_delete=models.CASCADE)
    auto_generate_recipe = models.BooleanField()
    linked_user = models.ForeignKey(User,on_delete=models.CASCADE, default = 1)
    create_date = models.DateField(default=timezone.now)

    #   Need to finish
    def __str__(self):
        price = round(self.cost_per_linear_yard_usd(), 2)
        return f'''{self.create_date} | Pricing: {self.fabric.end_customer} - {self.fabric.mill_name} | Fabric: {self.fabric.fabric_name} Price:{price}(USD/yd)'''


    def pricing_output(self):
        object_data = {
        'end_customer':self.fabric.end_customer,
        'mill_name':self.fabric.mill_name,
        'fabric_name':self.fabric.fabric_name,
        'fabric_weight':self.fabric.fabric_weight,
        'fabric_weight_unit':self.fabric.fabric_weight_unit,
        'fabric_width':self.fabric.fabric_width,
        'fabric_width_unit':self.fabric.fabric_width_unit,
        'recipe_name':self.recipe_name,
        'recipe_concentration':self.recipe_concentration,
        'linked_user':self.linked_user,
        'create_date':self.create_date}
        return object_data

    #  returns the fabric weight in terms of GSM regardless on input unit
    def get_fabric_gsm(self):
        if self.fabric.fabric_weight_unit == 'GSM':
            return self.fabric.fabric_weight
        else:
            return self.fabric.fabric_weight * self.ozyd_to_gsm

    #  return widths of the fabric in meters regardless of input unit
    def get_meter_width(self):
        if self.fabric.fabric_width_unit == 'CM':
            return self.fabric.fabric_width * 0.01
        else:
            return self.fabric.fabric_width * self.inches_to_meters

    #  returns total fabric weight in kilograms**
    def total_fabric_weight(self):
        return self.total_square_meters() * self.get_fabric_gsm() * self.gram_to_kilogram

    #  returns total chemical usage from minimum bath requirements
    def min_bath_chemical_usage(self):
       return ( self.minimum_bath * self.recipe_concentration.percent_total * self.percent_to_ratio / (self.wet_pick_up_percent * self.percent_to_ratio))

    #  returns strictly the chemistry used just to treat the fabric and nothing else
    def fabric_chemical_usage(self):
        return self.recipe_concentration.percent_total * self.percent_to_ratio * self.total_fabric_weight()


    #  returns the total chemical usage in KG for a production run
    def total_chemical_usage(self):
        return self.fabric_chemical_usage() + self.min_bath_chemical_usage()

    def get_list_price(self, recipe_type):
        return self.LIST_PRICES[recipe_type]

    def chemical_cost_per_kg(self):
        recipe_type = self.recipe_name.recipe_type
        return self.get_list_price(recipe_type)

    def chemical_cost_per_gram(self):
        return self.chemical_cost_per_kg() / self.kilogram_to_gram

    def grams_per_linear_yard(self):
        return self.get_meter_width() * self.yards_to_meters * self.get_fabric_gsm()

    #  returns the cost per yard in terms of RMB / YD
    def cost_per_linear_yard(self):
        return self.grams_per_linear_yard() * self.chemical_cost_per_gram() * self.recipe_concentration.percent_total() * self.percent_to_ratio

    def cost_per_linear_yard_usd(self):
        return self.cost_per_linear_yard() / self.get_usd_to_rmb()

    def get_usd_to_rmb(self):
        # link = 'https://free.currconv.com/api/v7/convert?q=USD_CNY&compact=ultra&apiKey=fca611f22855e782f663'
        # api_response = requests.get(link)
        # api_dict = json.loads(api_response.text)
        # print(api_dict)
        # usd_to_rmb = api_dict['USD_CNY']
        usd_to_rmb = 6.889 #placeholder price
        return usd_to_rmb


    def cost_form_dict(self):
        cost_form_output = {
        'price_per_kg_usd':round(self.chemical_cost_per_kg() / self.get_usd_to_rmb(), 2),
        'price_per_kg_rmb':round(self.chemical_cost_per_kg(), 2),
        'price_per_lb_usd':round(self.chemical_cost_per_kg() / self.kg_to_lb  / self.get_usd_to_rmb() , 2),
        'price_per_lb_rmb':round(self.chemical_cost_per_kg() / self.kg_to_lb , 2),
        'price_per_yard_rmb':round(self.cost_per_linear_yard(), 2),
        'price_per_yard_usd':round(self.cost_per_linear_yard_usd(), 2),
        'price_per_meter_rmb':round(self.cost_per_linear_yard() / self.yards_to_meters,2),
        'price_per_meter_usd':round(self.cost_per_linear_yard_usd() / self.yards_to_meters , 2),
        }
        return cost_form_output
