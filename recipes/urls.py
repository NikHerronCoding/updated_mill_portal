from django.urls import path
from recipes.views import MakeRecipes


app_name = 'recipes'
urlpatterns = [ path('update_recipes', MakeRecipes.as_view(), name='make_recipes'), ]
