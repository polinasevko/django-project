from django.shortcuts import render
from django.views.generic import DetailView
from .models import GuitarProduct, PianoProduct, MicProduct

# Create your views here.

def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):
    #context_obj_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    CT_MODEL_CLASS = {
        'guitarproduct': GuitarProduct,
        'pianoproduct': PianoProduct,
        'micproduct': MicProduct,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['content_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)