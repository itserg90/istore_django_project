from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(verbose_name='изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.FloatField(verbose_name='цена за покупку')
    created_at = models.DateField(verbose_name='дата создания(записи в БД)')
    updated_at = models.DateField(verbose_name='дата последнего изменения(записи в БД)')

    def __str__(self):
        return f'({self.name}, {self.description}, {self.image}, {self.price}, {self.created_at}, {self.updated_at})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Contacts(models.Model):
    country = models.CharField(max_length=100, verbose_name='страна')
    inn = models.IntegerField(verbose_name='инн')
    adress = models.TextField(verbose_name='адрес')

    def __str__(self):
        return f'{self.country}: {self.inn}, {self.adress}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
