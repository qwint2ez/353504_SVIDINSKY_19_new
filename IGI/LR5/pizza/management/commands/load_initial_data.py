from django.core.management.base import BaseCommand
from pizza.models import PizzaCategory, PizzaSize, Ingredient, Allergen

class Command(BaseCommand):
    help = 'Загрузка начальных данных'

    def handle(self, *args, **kwargs):
        # Категории
        categories = [
            {'name': 'Классические', 'description': 'Традиционные пиццы'},
            {'name': 'Вегетарианские', 'description': 'Пиццы без мяса'},
            {'name': 'Острые', 'description': 'Острые пиццы'},
        ]
        for cat in categories:
            PizzaCategory.objects.get_or_create(name=cat['name'], description=cat['description'])

        # Размеры
        sizes = [
            {'size': 'Маленькая (25 см)', 'multiplier': 1.0},
            {'size': 'Средняя (30 см)', 'multiplier': 1.3},
            {'size': 'Большая (35 см)', 'multiplier': 1.6},
        ]
        for size in sizes:
            PizzaSize.objects.get_or_create(size=size['size'], multiplier=size['multiplier'])

        # Ингредиенты
        ingredients = [
            {'name': 'Томатный соус', 'description': 'Классический томатный соус', 'is_vegetarian': True},
            {'name': 'Моцарелла', 'description': 'Сыр моцарелла', 'is_vegetarian': True},
            {'name': 'Пепперони', 'description': 'Острая салями', 'is_vegetarian': False},
            {'name': 'Грибы', 'description': 'Свежие шампиньоны', 'is_vegetarian': True},
            {'name': 'Ветчина', 'description': 'Ветчина из свинины', 'is_vegetarian': False},
            {'name': 'Лук', 'description': 'Свежий красный лук', 'is_vegetarian': True},
            {'name': 'Перец', 'description': 'Болгарский перец', 'is_vegetarian': True},
        ]
        for ing in ingredients:
            Ingredient.objects.get_or_create(
                name=ing['name'],
                description=ing['description'],
                is_vegetarian=ing['is_vegetarian']
            )

        # Аллергены
        allergens = [
            {'name': 'Глютен', 'description': 'Содержит глютен'},
            {'name': 'Лактоза', 'description': 'Содержит молочные продукты'},
            {'name': 'Яйца', 'description': 'Содержит яйца'},
            {'name': 'Орехи', 'description': 'Содержит орехи'},
        ]
        for alg in allergens:
            Allergen.objects.get_or_create(name=alg['name'], description=alg['description'])

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
