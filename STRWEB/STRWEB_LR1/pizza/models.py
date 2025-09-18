from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal

def validate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError('Возраст должен быть не менее 18 лет')

class PizzaCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Allergen(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PizzaSize(models.Model):
    size = models.CharField(max_length=20)  # Small, Medium, Large
    multiplier = models.DecimalField(max_digits=4, decimal_places=2)  # Price multiplier
    
    def __str__(self):
        return self.size

class SeasonalPeriod(models.Model):
    name = models.CharField(max_length=100)  # например, "Лето 2023"
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name
    
class Pizza(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(PizzaCategory, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    sauce = models.CharField(max_length=100, verbose_name="Соус")
    is_vegan = models.BooleanField(default=False, verbose_name="Вегетарианская")
    ingredients = models.ManyToManyField(Ingredient, verbose_name="Ингредиенты")
    allergens = models.ManyToManyField(Allergen, verbose_name="Аллергены")
    available_sizes = models.ManyToManyField(PizzaSize, through='PizzaPricing', verbose_name="Доступные размеры")
    image = models.ImageField(upload_to='pizzas/', null=True, blank=True, verbose_name="Изображение")  # добавлено поле для фото

    def __str__(self):
        return self.name

    def get_base_price(self):
        pricing = self.pizzapricing_set.order_by('price').first()
        return pricing.price if pricing else None

class PizzaPricing(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")

    class Meta:
        unique_together = ('pizza', 'size')

    def __str__(self):
        return f"{self.pizza.name} - {self.size.size} - {self.price}₽"
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
        message="Номер телефона должен быть в формате: '+375 (29) XXX-XX-XX'"
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=19,
        help_text="Формат: +375 (29) XXX-XX-XX"
    )
    address = models.TextField()
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        validators=[validate_age],
        help_text='Должно быть 18+ лет',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.birth_date:  # Проверяем возраст только если дата указана
            validate_age(self.birth_date)

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_orders = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    is_available = models.BooleanField(default=True)
    working_hours = models.JSONField(default=dict)  # График работы

    def __str__(self):
        return self.user.username

    def update_earnings(self, amount):
        self.earnings += amount
        self.completed_orders += 1
        self.save()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    promo_code = models.ForeignKey('Promo', on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='pending')
    pizzas = models.ManyToManyField(Pizza, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
    def get_local_created_at(self):
        return timezone.localtime(self.created_at).strftime('%d/%m/%Y %H:%M:%S')
    
    def get_utc_created_at(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M:%S')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.pizza.name} x {self.quantity}"

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    history = models.TextField()
    requisites = models.TextField()
    founding_year = models.IntegerField()
    mission = models.TextField()
    video_url = models.FileField(null=True, blank=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)  # Новое поле
    employees = models.ManyToManyField('Employee', related_name='company')

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Review by {self.customer}"

class Promo(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)  # Делаем поле опциональным
    description = models.TextField(blank=True, null=True)  # Делаем поле опциональным
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    customers = models.ManyToManyField(Customer, related_name='promos', blank=True)
    
    def __str__(self):
        return self.code

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class CustomerPreferences(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='preferences')
    favorite_pizzas = models.ManyToManyField(Pizza)
    allergies = models.ManyToManyField(Allergen)
    preferred_payment_method = models.CharField(max_length=50)
    newsletter_subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.customer}"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)  # Новое поле
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        validators=[validate_age],
        help_text='Должно быть 18+ лет',
        null=True,  # Добавляем эти два параметра
        blank=True  # чтобы поле стало опциональным
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    def clean(self):
        super().clean()
        if self.birth_date:
            validate_age(self.birth_date)

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PartnerCompany(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        base_price = self.pizza.get_base_price()
        return base_price * self.quantity if base_price else 0