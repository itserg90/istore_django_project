from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Contact, Version, Category
from catalog.services import get_categories_from_cache


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/categories.html'

    def get_queryset(self):
        return get_categories_from_cache()


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

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.request.user == self.object.user or self.request.user.is_superuser:
    #         return self.object
    #     raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', args=[self.kwargs.get('slug')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = ProductFormSet(self.request.POST, instance=self.object)
        else:
            formset = ProductFormSet(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if user.has_perm("catalog.unpublished"):
            return ProductModeratorForm
        raise PermissionDenied


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
