from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pizza.models import (
    Pizza, PizzaCategory, Ingredient, Allergen,
    PizzaSize, PizzaPricing
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Загрузка демонстрационных данных'

    def handle(self, *args, **kwargs):
        # Создаем администратора если его нет
        User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )[0].set_password('admin')

        # Пиццы и их данные
        pizzas_data = [
            {
                'name': 'Пепперони',
                'description': 'Классическая пицца с пепперони и моцареллой',
                'price': Decimal('15.99'),
                'sauce': 'Томатный',
            },
            {
                'name': 'Маргарита',
                'description': 'Традиционная итальянская пицца с томатами и моцареллой',
                'price': Decimal('12.99'),
                'sauce': 'Томатный',
            },
            {
                'name': 'Гавайская',
                'description': 'Пицца с ветчиной и ананасами',
                'price': Decimal('16.99'),
                'sauce': 'Томатный',
            },
            {
                'name': '4 сыра',
                'description': 'Пицца с четырьмя видами сыра',
                'price': Decimal('18.99'),
                'sauce': 'Сливочный',
            },
            {
                'name': 'Вегетарианская',
                'description': 'Пицца с грибами, перцем и луком',
                'price': Decimal('14.99'),
                'sauce': 'Томатный',
            },
            {
                'name': 'Мясная',
                'description': 'Пицца с тремя видами мяса',
                'price': Decimal('19.99'),
                'sauce': 'Барбекю',
            },
            {
                'name': 'Грибная',
                'description': 'Пицца с тремя видами грибов',
                'price': Decimal('15.99'),
                'sauce': 'Сливочный',
            },
            {
                'name': 'Диабло',
                'description': 'Острая пицца с халапеньо',
                'price': Decimal('17.99'),
                'sauce': 'Острый томатный',
            },
            {
                'name': 'Морская',
                'description': 'Пицца с морепродуктами',
                'price': Decimal('21.99'),
                'sauce': 'Сливочный',
            },
            {
                'name': 'Барбекю',
                'description': 'Пицца с курицей и соусом барбекю',
                'price': Decimal('16.99'),
                'sauce': 'Барбекю',
            },
        ]

        # Создаем пиццы
        for pizza_data in pizzas_data:
            pizza, created = Pizza.objects.get_or_create(
                name=pizza_data['name'],
                defaults={
                    'description': pizza_data['description'],
                    'price': pizza_data['price'],
                    'sauce': pizza_data['sauce'],
                    'category': PizzaCategory.objects.first()
                }
            )
            
            # Добавляем ингредиенты
            if created:
                pizza.ingredients.add(*Ingredient.objects.all()[:3])
                pizza.allergens.add(*Allergen.objects.all()[:2])
                
                # Создаем цены для разных размеров
                for size in PizzaSize.objects.all():
                    # Преобразуем float в Decimal перед умножением
                    multiplier = Decimal(str(size.multiplier))
                    PizzaPricing.objects.create(
                        pizza=pizza,
                        size=size,
                        price=pizza_data['price'] * multiplier
                    )

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные успешно загружены'))
