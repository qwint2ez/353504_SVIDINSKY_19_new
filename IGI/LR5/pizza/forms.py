from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Pizza, Order, Review, Customer, validate_age  # добавляем импорт validate_age
from datetime import date

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
    phone = forms.CharField(
        max_length=19,
        help_text="Формат: +375 (29) XXX-XX-XX",
        validators=[Customer.phone_regex]
    )
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения',
        help_text='Для регистрации вам должно быть 18 лет или больше'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('Вам должно быть 18 лет или больше для регистрации')
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=True)
        Customer.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address'],
            birth_date=self.cleaned_data.get('birth_date')
        )
        return user
