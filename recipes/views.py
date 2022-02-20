from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Recipe, Category, Ingredient

categories = (('Супы', 'supy'),
              ('Выпечка', 'vypechka'),
              ('Десерет', 'deseret'),
              ('Вторые блюда', 'vtorye-blyuda'),
              ('Салаты', 'salaty'),
              ('Напитки', 'napitki'))


class List(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        return context


class RecipeList(List):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q'):
            context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Recipe.objects.filter(
                Q(name__icontains=query) | Q(ingredient__name__icontains=query) | Q(category__name__icontains=query))\
                .select_related('category').prefetch_related('ingredient').distinct().order_by('-updated_at')
        return Recipe.objects.all().select_related('category').prefetch_related('ingredient').order_by('-updated_at')


class IngredientList(List):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient = Ingredient.objects.get(slug=self.kwargs['ingredient_slug'])
        context['ingredient'] = ingredient
        return context

    def get_queryset(self):
        return Recipe.objects.filter(ingredient__slug=self.kwargs['ingredient_slug']) \
            .select_related('category').prefetch_related('ingredient').order_by('-updated_at')


class CategoryList(List):
    template_name = 'recipes/category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        context['category'] = category
        return context

    def get_queryset(self):
        return Recipe.objects.filter(category__slug=self.kwargs['category_slug']) \
            .select_related('category').prefetch_related('ingredient').order_by('-updated_at')


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    slug_url_kwarg = 'recipe_slug'
    pk_url_kwarg = 'recipe_pk'
    context_object_name = 'recipe'
