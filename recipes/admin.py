from django.contrib import admin

from .models import Ingredient, Recipe, Category


class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}


class RecipeAdmin(BaseAdmin):
    list_display = ('id', 'name', 'category', 'created_at', 'updated_at')
    filter_horizontal = ('ingredient',)
    search_fields = ('name', 'ingredient__name__icontains', 'category__name__icontains')


admin.site.register(Ingredient, BaseAdmin)
admin.site.register(Category, BaseAdmin)
admin.site.register(Recipe, RecipeAdmin)
