import json

from django.shortcuts import render
from catalog.models import Category, Product, Contacts


data_contacts = {}
for contact in Contacts.objects.all():
    data_contacts['country'] = contact.country
    data_contacts['inn'] = contact.inn
    data_contacts['adress'] = contact.adress


def json_read_products():
    list_of_products = []

    with open('data.json') as file:
        for element in json.load(file):
            if element['model'] == 'catalog.product':
                list_of_products.append(element['fields'])
    return list_of_products


data_json = json_read_products()


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        print(f'{name}: {price}')
    return render(request, 'catalog/home.html', {'products': data_json})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f'{name} - {phone}: {message}')

    return render(request, 'catalog/contacts.html', {'contacts': data_contacts})
