from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pizza, Order, Review, Customer

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'description', 'price', 'sauce', 'image', 
                 'ingredients', 'allergens', 'category', 'available_sizes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'ingredients': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'allergens': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'available_sizes': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '3'
            })
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_date']
        widgets = {
            'delivery_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'].label = 'Время доставки'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['pizza', 'rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=True)
        Customer.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address']
        )
        return user
