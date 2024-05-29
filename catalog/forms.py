from django.forms import ModelForm, ValidationError, BooleanField

from catalog.models import Product, Version


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'category', 'is_published']

    FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                       'радар']

    def check_words(self, text):
        if any(word in text.lower() for word in self.FORBIDDEN_WORDS):
            raise ValidationError(f'Текст не должен содержать слова: {self.FORBIDDEN_WORDS}')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        self.check_words(cleaned_data)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        self.check_words(cleaned_data)
        return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version', 'name', 'current_version']

    def clean_current_version(self):
        current_v = Version.objects.filter(current_version=True).filter(product=self.cleaned_data.get('product'))
        cleaned_data = self.cleaned_data.get('current_version')
        if current_v and cleaned_data:
            raise ValidationError(
                'Может быть указана только одна активная версия.'
                '(Для изменения активной версии, сначала сохраните Продукт без активной версии.)')
        return cleaned_data
