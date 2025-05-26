from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .models import Pizza, Order, Review, Customer, validate_age, PizzaPricing, PizzaSize, Ingredient, Allergen  # добавляем импорт validate_age
from datetime import date, datetime, timedelta
from django.forms import inlineformset_factory
from django.utils import timezone

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'pattern': '[A-Za-zА-Яа-яЁё\s]{2,50}',
            'title': 'Название должно содержать от 2 до 50 букв',
            'required': 'required'
        })
        self.fields['description'].widget.attrs.update({
            'minlength': '20',
            'maxlength': '500',
            'required': 'required'
        })
        self.fields['base_price'].widget.attrs.update({
            'min': '0',
            'step': '0.01',
            'required': 'required'
        })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Название должно содержать минимум 2 символа")
        return name

    def save(self, commit=True):
        pizza = super().save(commit=True)
        base_price = self.cleaned_data['base_price']
        
        # Удаляем существующие цены перед созданием новых
        PizzaPricing.objects.filter(pizza=pizza).delete()
        
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
        # Используем timezone.now() вместо datetime.now()
        min_delivery = timezone.now() + timedelta(hours=1)
        max_delivery = timezone.now() + timedelta(days=7)
        
        self.fields['delivery_date'].widget.attrs.update({
            'min': min_delivery.strftime('%Y-%m-%dT%H:%M'),
            'max': max_delivery.strftime('%Y-%m-%dT%H:%M')
        })
        self.fields['delivery_date'].label = 'Время доставки'

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if not delivery_date:
            raise forms.ValidationError("Это поле обязательно")
            
        # Преобразуем в aware datetime
        min_delivery = timezone.now() + timedelta(hours=1)
        max_delivery = timezone.now() + timedelta(days=7)
        
        if delivery_date < min_delivery:
            raise forms.ValidationError("Время доставки должно быть как минимум через час")
        if delivery_date > max_delivery:
            raise forms.ValidationError("Время доставки не может быть более чем через неделю")
        return delivery_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['pizza', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'type': 'number',
                'min': '1',
                'max': '5',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'minlength': '10',
                'maxlength': '500'
            })
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:  # проверяем что значение существует
            try:
                rating = int(rating)  # преобразуем в число
                if rating < 1 or rating > 5:
                    raise forms.ValidationError('Рейтинг должен быть от 1 до 5')
            except (TypeError, ValueError):
                raise forms.ValidationError('Введите корректное число')
        return rating

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(
        max_length=19,
        help_text="Формат: +375 (29) XXX-XX-XX",
        validators=[
            RegexValidator(
                regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
                message="Номер телефона должен быть в формате: '+375 (29) XXX-XX-XX'"
            )
        ]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'pattern': '[A-Za-z0-9@.+-_]{4,150}',
            'title': 'Имя пользователя должно содержать от 4 до 150 символов',
            'required': 'required'
        })
        self.fields['email'].widget.attrs.update({
            'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
            'title': 'Введите корректный email',
            'required': 'required'
        })
        self.fields['phone'].widget.attrs.update({
            'pattern': '\+375 \([0-9]{2}\) [0-9]{3}-[0-9]{2}-[0-9]{2}',
            'title': 'Формат: +375 (XX) XXX-XX-XX',
            'required': 'required'
        })
        self.fields['birth_date'].widget.attrs.update({
            'max': (date.today() - timedelta(days=365*18)).isoformat(),
            'required': 'required'
        })

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('Вам должно быть 18 лет или больше для регистрации')
        return birth_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Это поле обязательно.')
        return phone

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
