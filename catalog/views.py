from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Contact


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'name'
        context['phone'] = 'phone'
        context['message'] = 'message'
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['name'] = request.POST.get("name")
        context['phone'] = request.POST.get("phone")
        context['message'] = request.POST.get("message")
        c = Contact(name=context['name'], phone=context['phone'], message=context['message'])
        c.save()
        return render(request, 'catalog/contacts.html', context)
