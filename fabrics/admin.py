from django.contrib import admin
from fabrics import models
# Register your models here.

admin.site.register(models.Fabric)
admin.site.register(models.FabricComposition)
admin.site.register(models.CompositionsInFabric)
admin.site.register(models.Mill)
admin.site.register(models.UserToMill)
admin.site.register(models.Address)




