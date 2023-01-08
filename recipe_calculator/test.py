from recipe_calculator.models import RecipeCalculator
from fabrics.models import Fabric, CompositionsInFabric



def test_1():
    recipe_calculator = RecipeCalculator()
    fabric = Fabric.objects.all()[0]
    recipe_calculator.fabric = fabric
    recipe_calculator.save()
    return recipe_calculator.calculate_percent_synthetic

def test_2():
    recipe_calculator = RecipeCalculator()
    fabric = Fabric.objects.all()[0]
    recipe_calculator.fabric = fabric
    recipe_calculator.save(commit=False)
    return recipe_calculator.calculate_percent_synthetic

