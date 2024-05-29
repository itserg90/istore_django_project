from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Product, Contact, Version


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['products'] = []
        for product_object in context_data['object_list']:
            current_version = Version.objects.filter(current_version=True).filter(product=product_object)
            if current_version:
                context_data['products'].append((current_version[0], product_object))
            else:
                context_data['products'].append(({'version': 'Нет активной версии'}, product_object))
        return context_data


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_name = form.save()
    #         new_name.slug = slugify(new_name.title)
    #         new_name.save()
    #
    #     return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_list', args=[self.kwargs.get('pk')])


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
