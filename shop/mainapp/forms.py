from django import forms
from .models import Order, User


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment',
        )


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} is not found.')
        user = User.objects.filter(username=username).first()
        if not user.check_password(password):
            raise forms.ValidationError(f'Password is incorrect.')
        return self.cleaned_data

    class Meta:
        model = User
        fields = (
            'username', 'password'
        )


class SignInForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} has already been taken.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} has already been taken.')
        return username

    def clean(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data

    class Meta:
        model = User
        fields = (
            'username', 'password', 'confirm_password', 'first_name', 'last_name', 'phone', 'email',
        )
