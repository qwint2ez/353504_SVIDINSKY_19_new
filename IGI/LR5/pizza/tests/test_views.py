import pytest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from pizza.models import Pizza, PizzaCategory, Customer
from datetime import date, timedelta

@pytest.mark.django_db
class TestPizzaViews:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def test_category(self):
        return PizzaCategory.objects.create(name="Тестовая категория")

    @pytest.fixture
    def test_pizza(self, test_category):
        return Pizza.objects.create(
            name="Тестовая пицца",
            description="Описание",
            category=test_category,
            price=10.00  # Добавляем обязательное поле цены
        )

    def test_pizza_list_view(self, client, test_pizza):
        response = client.get(reverse('pizza:pizza_list'))
        assert response.status_code == 200
        assert test_pizza.name.encode() in response.content

    def test_pizza_detail_view(self, client, test_pizza):
        response = client.get(
            reverse('pizza:pizza_detail', kwargs={'pk': test_pizza.pk})
        )
        assert response.status_code == 200
        assert test_pizza.name.encode() in response.content

class TestOrderViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            birth_date=date.today() - timedelta(days=365*20)
        )
        self.category = PizzaCategory.objects.create(name="Тест")
        self.pizza = Pizza.objects.create(
            name="Тест пицца",
            description="Описание",
            category=self.category,
            price=10.00  # Добавляем обязательное поле цены
        )

    def test_order_creation_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('pizza:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_order_creation_unauthenticated(self):
        response = self.client.get(reverse('pizza:order_create'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
