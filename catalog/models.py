from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(verbose_name='изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.FloatField(verbose_name='цена за покупку')
    created_at = models.DateField(verbose_name='дата создания(записи в БД)')
    updated_at = models.DateField(verbose_name='дата последнего изменения(записи в БД)')
    manufactured_at = models.DateField(verbose_name='дата производства', default=None)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
