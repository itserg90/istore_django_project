from django.forms import ModelForm, ValidationError

from catalog.models import Product


class ProductForm(ModelForm):
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

