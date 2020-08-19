
# Register your models here.

from django.contrib import admin
from .models import RecipeConcentration, RecipeName

admin.site.register(RecipeConcentration)
admin.site.register(RecipeName)

