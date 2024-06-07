import json

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product


class Command(BaseCommand):
    Category.objects.all().delete()
    Product.objects.all().delete()

    @staticmethod
    def json_read_categories_and_products():
        with open('data1.json') as file:
            return json.load(file)

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        categories_for_create = []
        products_for_create = []

        for element in Command.json_read_categories_and_products():
            if element['model'] == 'catalog.category':
                category = element['fields']
                categories_for_create.append(Category(**category))

        Category.objects.bulk_create(categories_for_create)
        for element in Command.json_read_categories_and_products():
            if element['model'] == 'catalog.product':
                product = element['fields']
                products_for_create.append(Product(name=product['name'],
                                                   slug=product['slug'],
                                                   description=product['description'],
                                                   image=product['image'],
                                                   category=Category.objects.get(pk=product['category']),
                                                   price=product['price'],
                                                   created_at=product['created_at'],
                                                   updated_at=product['updated_at']))
        Product.objects.bulk_create(products_for_create)
