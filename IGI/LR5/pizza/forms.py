from django import forms
from .models import Pizza, Order, Review

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
        fields = ['customer', 'delivery_date']
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
