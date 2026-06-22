from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150, label='Full Name')
    email = forms.EmailField(label='Email Address')
    address = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'rows': 2}))
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20, label='Postal Code')


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience…'}),
        }


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(
        attrs={'placeholder': 'Search products…'}
    ))
