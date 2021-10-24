from django.contrib import admin
from django.forms import ModelChoiceField
from .models import *


class GuitarAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='guitars'))
        else:
            return super().formfield_for_foreignkey(db_field, request, kwargs)


class PianoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='piano'))
        else:
            return super().formfield_for_foreignkey(db_field, request, kwargs)


class MicAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='mics'))
        else:
            return super().formfield_for_foreignkey(db_field, request, kwargs)


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(MicProduct, MicAdmin)
admin.site.register(PianoProduct, PianoAdmin)
admin.site.register(GuitarProduct, GuitarAdmin)
admin.site.register(Customer)
admin.site.register(Order)
