from django.db import models
from django.urls import reverse


class TimeStampMixin(models.Model):
    """Реализация атрибутов времени создания и обновления записи"""

    created_at = models.DateTimeField('Время создания записи', auto_now_add=True)
    updated_at = models.DateTimeField('Время обновления записи', auto_now=True)

    class Meta:
        abstract = True


class Ingredient(TimeStampMixin):
    """Ингридиенты"""
    name = models.CharField('Название', max_length=150, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredient', kwargs={'ingredient_slug': self.slug})

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']


class Category(TimeStampMixin):
    """Категории"""
    name = models.CharField('Название', max_length=150, unique=True)
    image = models.ImageField(upload_to=f'image/category/%Y/%m/%d/', verbose_name='Изображение', null=True, blank=True)
    description = models.TextField('Описание')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Recipe(TimeStampMixin):
    """Рецепты"""
    name = models.CharField('Название', max_length=150)
    ingredient = models.ManyToManyField(Ingredient,
                                        related_name='recipe_ingredient',
                                        verbose_name='Ингридиенты')
    category = models.ForeignKey(Category,
                                 related_name='recipe_category',
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 null=True)
    image = models.ImageField(upload_to=f'image/recipe/%Y/%m/%d/', verbose_name='Изображение', null=True, blank=True)
    recipe_text = models.TextField('Рецепт')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_slug': self.slug})

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']
