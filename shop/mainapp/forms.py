from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'status', 'order_date', 'comment',
        )


class LoginForm(forms.ModelForm):

