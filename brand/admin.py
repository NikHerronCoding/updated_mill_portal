from django.contrib import admin
from brand import models
# Register your models here.

admin.site.register(models.Country)
admin.site.register(models.Brand)
admin.site.register(models.UserToBrand)