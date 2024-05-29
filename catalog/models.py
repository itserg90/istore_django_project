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
    slug = models.CharField(max_length=100, verbose_name='slug', null=True, blank=True)
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(verbose_name='изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.FloatField(verbose_name='цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания(записи в БД)')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения(записи в БД)')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(verbose_name='просмотры', default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    message = models.TextField(verbose_name='сообщение')

    def __str__(self):
        return f'({self.name}, {self.phone}, {self.message})'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Продукт')
    version = models.CharField(max_length=50, verbose_name='Версия')
    name = models.CharField(max_length=100, verbose_name='имя')
    current_version = models.BooleanField(default=False, verbose_name='активная версия')

    class Meta:
        verbose_name = 'версия продукта'
        verbose_name_plural = 'версии продукта'

    def __str__(self):
        return f'({self.product}, {self.version}, {self.name}, {self.current_version})'
