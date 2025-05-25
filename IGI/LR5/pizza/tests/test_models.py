import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from pizza.models import Pizza, PizzaCategory, Customer
from datetime import date, timedelta

@pytest.mark.django_db
class TestPizzaModel:
    def test_pizza_creation(self):
        category = PizzaCategory.objects.create(name="Тестовая")
        pizza = Pizza.objects.create(
            name="Тестовая пицца",
            description="Описание",
            category=category,
            price=10.00  # Добавляем обязательное поле цены
        )
        assert pizza.name == "Тестовая пицца"
        assert str(pizza) == "Тестовая пицца"

    @pytest.mark.parametrize("name,description,price", [
        ("Маргарита", "Классическая", 10.00),
        ("Пепперони", "Острая", 12.00),
    ])
    def test_pizza_variants(self, name, description, price):
        category = PizzaCategory.objects.create(name="Тест")
        pizza = Pizza.objects.create(
            name=name,
            description=description,
            category=category,
            price=price
        )
        assert pizza.name == name
        assert pizza.price == price

class TestCustomerModel(TestCase):
    def test_customer_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        customer = Customer.objects.create(
            user=user,
            birth_date=date.today() - timedelta(days=365*20)
        )
        self.assertEqual(str(customer), 'testuser')
