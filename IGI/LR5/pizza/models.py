from django.db import models
from django.contrib.auth.models import User

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
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sauce = models.CharField(max_length=50)
    image = models.ImageField(upload_to='pizzas/', null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    allergens = models.ManyToManyField(Allergen)
    chef = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_pizzas')
    recommended_with = models.ManyToManyField('self', blank=True)
    category = models.ForeignKey(PizzaCategory, on_delete=models.SET_NULL, null=True)
    available_sizes = models.ManyToManyField(PizzaSize, through='PizzaPricing')
    seasonal_availability = models.ManyToManyField(
        'SeasonalPeriod',
        related_name='available_pizzas',
        blank=True
    )
    
    def __str__(self):
        return self.name

class PizzaPricing(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('pizza', 'size')

    def __str__(self):
        return f"{self.pizza.name} - {self.size.size}: {self.price}"
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return self.user.username

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username

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
    
    def __str__(self):
        return f"Order {self.id} by {self.customer}"

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
    employees = models.ManyToManyField('Employee', related_name='company')
    founding_year = models.IntegerField()
    mission = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    
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
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
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
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"