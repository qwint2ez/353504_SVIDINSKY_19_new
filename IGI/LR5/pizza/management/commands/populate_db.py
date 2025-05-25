from django.core.management.base import BaseCommand
from pizza.models import Pizza, PizzaCategory, PizzaSize, PizzaPricing
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        # Создаем категории
        categories = {
            'Классические': 'Традиционные итальянские пиццы',
            'Мясные': 'Пиццы с мясными начинками',
            'Вегетарианские': 'Пиццы без мяса',
            'Острые': 'Острые пиццы',
        }
        
        for name, desc in categories.items():
            PizzaCategory.objects.get_or_create(
                name=name,
                description=desc
            )

        # Создаем размеры, если их нет
        sizes = {
            'Маленькая 25см': Decimal('0.8'),
            'Средняя 30см': Decimal('1.0'),
            'Большая 35см': Decimal('1.2'),
        }
        
        for name, mult in sizes.items():
            PizzaSize.objects.get_or_create(
                size=name,
                multiplier=mult
            )

        # Список пицц
        pizzas = [
            {
                'name': 'Маргарита',
                'description': 'Классическая итальянская пицца с томатами и моцареллой',
                'category': 'Классические',
                'price': Decimal('15.00'),
            },
            {
                'name': 'Пепперони',
                'description': 'Острая пицца с колбасой пепперони',
                'category': 'Острые',
                'price': Decimal('18.00'),
            },
            # Добавьте еще 8+ пицц
        ]

        # Создаем пиццы
        for pizza_data in pizzas:
            category = PizzaCategory.objects.get(name=pizza_data['category'])
            pizza, created = Pizza.objects.get_or_create(
                name=pizza_data['name'],
                defaults={
                    'description': pizza_data['description'],
                    'category': category,
                    'price': pizza_data['price'],
                }
            )
            
            if created:
                # Добавляем размеры и цены
                for size in PizzaSize.objects.all():
                    pizza.available_sizes.add(size)
                    PizzaPricing.objects.create(
                        pizza=pizza,
                        size=size,
                        price=pizza_data['price'] * size.multiplier
                    )

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
