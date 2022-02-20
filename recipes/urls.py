from django.urls import path

from .views import RecipeList, RecipeDetail, IngredientList, CategoryList

urlpatterns = [
    path('', RecipeList.as_view(), name='home'),
    path('recipe/<slug:recipe_slug>/', RecipeDetail.as_view(), name='recipe'),
    path('ingredient/<slug:ingredient_slug>/', IngredientList.as_view(), name='ingredient'),
    path('category/<slug:category_slug>/', CategoryList.as_view(), name='category'),
]
