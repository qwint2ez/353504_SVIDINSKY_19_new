import pytest
from django.test import TestCase
from pizza.forms import UserRegistrationForm
from datetime import date, timedelta

class TestUserRegistrationForm(TestCase):
    def test_valid_registration(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',  # Более сложный пароль
            'password2': 'StrongPass123!',
            'birth_date': date.today() - timedelta(days=365*20),
            'phone': '+375 (29) 123-45-67',  # Правильный формат телефона
            'address': 'Test Address'
        }
        form = UserRegistrationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Для отладки
        self.assertTrue(form.is_valid())

    def test_invalid_age(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123!@#',
            'password2': 'testpass123!@#',
            'birth_date': date.today() - timedelta(days=365*17),
            'phone': '+375291234567',
            'address': 'Test Address'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
