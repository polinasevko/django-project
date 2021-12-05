from django import forms
from mainapp.models import Category, Product
from .models import CategoryFeature, ProductFeature


class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class NewCategoryFeatureForm(forms.ModelForm):
    class Meta:
        model = CategoryFeature
        fields = '__all__'


class FeatureToProductForm(forms.ModelForm):
    def __init__(self, *args, category=None, **kwargs):
        super(FeatureToProductForm, self).__init__(*args, **kwargs)
        if category:
            self.fields['feature'].queryset = self.fields['feature'].queryset.filter(category__name__contains=category)
            self.fields['product'].queryset = self.fields['product'].queryset.filter(category__name__contains=category)

    class Meta:
        model = ProductFeature
        fields = '__all__'