from django.shortcuts import render
from django.views import View
from .forms import NewCategoryForm, NewCategoryFeatureForm
from django.http import HttpResponseRedirect


class BaseSpecView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'product_spec.html', {})


class NewCategoryView(View):
    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/spec/')
        return render(request, 'new_category.html', context)


class CreateNewFeatureView(View):
    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            new_feature = form.save(commit=False)
            new_feature.category = form.cleaned_data['category']
            new_feature.feature_type = form.cleaned_data['feature_type']
            new_feature.save()
            return HttpResponseRedirect('/spec/')
        return render(request, 'new_feature.html', context)
