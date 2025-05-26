import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from pizza.models import Pizza, PizzaCategory, Customer, PizzaSize, PizzaPricing
from decimal import Decimal
from datetime import date, timedelta

@pytest.mark.django_db
class TestPizzaModel:
    def test_pizza_creation(self):
        # Создаем категорию
        category = PizzaCategory.objects.create(name="Тестовая")
        
        # Создаем размер
        size = PizzaSize.objects.create(size="Средняя (30 см)", multiplier=Decimal('1.0'))
        
        # Создаем пиццу
        pizza = Pizza.objects.create(
            name="Тестовая пицца",
            description="Описание",
            category=category,
            sauce="Томатный",
            is_vegan=False
        )
        
        # Создаем цену для пиццы
        pricing = PizzaPricing.objects.create(
            pizza=pizza,
            size=size,
            price=Decimal('10.00')
        )

        assert pizza.name == "Тестовая пицца"
        assert str(pizza) == "Тестовая пицца"
        assert pizza.get_base_price() == Decimal('10.00')

    @pytest.mark.parametrize("name,description,base_price", [
        ("Маргарита", "Классическая", Decimal('10.00')),
        ("Пепперони", "Острая", Decimal('12.00')),
    ])
    def test_pizza_variants(self, name, description, base_price):
        category = PizzaCategory.objects.create(name="Тест")
        size = PizzaSize.objects.create(size="Средняя (30 см)", multiplier=Decimal('1.0'))
        
        pizza = Pizza.objects.create(
            name=name,
            description=description,
            category=category,
            sauce="Томатный",
            is_vegan=False
        )
        
        pricing = PizzaPricing.objects.create(
            pizza=pizza,
            size=size,
            price=base_price
        )

        assert pizza.name == name
        assert pizza.get_base_price() == base_price

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
