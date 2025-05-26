from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Pizza, Order, Review, Customer, validate_age, PizzaPricing, PizzaSize, Ingredient, Allergen  # добавляем импорт validate_age
from datetime import date
from django.forms import inlineformset_factory

class PizzaForm(forms.ModelForm):
    base_price = forms.DecimalField(
        label='Базовая цена (для среднего размера)',
        min_value=0,
        help_text='Цены для других размеров будут рассчитаны автоматически'
    )

    class Meta:
        model = Pizza
        fields = ['name', 'description', 'category', 'sauce', 'is_vegan', 'ingredients', 'allergens']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.CheckboxSelectMultiple(attrs={'class': 'ingredients-list'}),
            'allergens': forms.CheckboxSelectMultiple(attrs={'class': 'allergens-list'}),
        }

    def save(self, commit=True):
        pizza = super().save(commit=True)
        base_price = self.cleaned_data['base_price']
        
        # Создаем цены для всех размеров
        sizes = PizzaSize.objects.all()
        for size in sizes:
            PizzaPricing.objects.create(
                pizza=pizza,
                size=size,
                price=base_price * size.multiplier
            )
        return pizza

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

# Новая форма для цен
PizzaPricingFormSet = inlineformset_factory(
    Pizza, 
    PizzaPricing,
    fields=['size', 'price'],
    extra=1,
    can_delete=True
)
