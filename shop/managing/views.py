from django.shortcuts import render
from django.views import View
from .forms import NewCategoryForm, NewCategoryFeatureForm, FeatureToProductForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin
from mainapp.models import Category
from .models import ProductFeature
from django.contrib import messages


class BaseManagingView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'managing.html', context)


class CreateNewCategoryView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/managing/')
        return render(request, 'new_category.html', context)


class CreateNewFeatureView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            new_feature = form.save(commit=False)
            new_feature.category = form.cleaned_data['category']
            new_feature.feature_type = form.cleaned_data['feature_type']
            new_feature.save()
            return HttpResponseRedirect('/managing/')
        return render(request, 'new_feature.html', context)


class SelectCategoryView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'select-category.html', context)


class FeatureToProductView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        form = FeatureToProductForm(request.POST or None, category=category)
        context = {'curr_category': category, 'form': form}
        return render(request, 'feature-to-product.html', context)

    def post(self, request, *args, **kwargs):
        form = FeatureToProductForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            feature = form.cleaned_data['feature']
            product = form.cleaned_data['product']
            product_feature, created = ProductFeature.objects.get_or_create(feature=feature, product=product)
            if created:
                product_feature.value = form.cleaned_data['value']
                product_feature.save()
                return HttpResponseRedirect('/managing/')
            else:
                messages.add_message(request, messages.ERROR, f'A {product} with specification {feature} already exists.')
                return HttpResponseRedirect('/managing/feature-to-product/select-category/')
        return render(request, 'feature-to-product.html', context)
