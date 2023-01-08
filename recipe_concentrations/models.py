from django.db import models

#this class gives the ratio of each component in a named recipe along with its concentration name and recipe type
class RecipeConcentration(models.Model):
    recipe_type = models.CharField(default="NORR", max_length=16)
    concentration = models.CharField(max_length=16)
    percent_1 = models.FloatField()
    percent_2 = models.FloatField()
    percent_3 = models.FloatField()
    percent_4 = models.FloatField()
    percent_5 = models.FloatField()
    percent_6 = models.FloatField()

    def __str__(self):
        return f"{self.recipe_type} {self.concentration}"

    def percent_total(self):
        sum_percent = [self.percent_1, self.percent_2, self.percent_3, self.percent_4, self.percent_5, self.percent_6]
        return sum(sum_percent)