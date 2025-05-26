from django.core.management.base import BaseCommand
from pizza.models import (
    PizzaCategory, PizzaSize, Pizza, PizzaPricing,
    Ingredient, Allergen
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Reset and load initial data'

    def handle(self, *args, **kwargs):
        # Очищаем все данные
        PizzaPricing.objects.all().delete()
        Pizza.objects.all().delete()
        PizzaSize.objects.all().delete()
        PizzaCategory.objects.all().delete()
        Ingredient.objects.all().delete()
        Allergen.objects.all().delete()

        # Создаем размеры
        sizes = [
            {'size': 'Большая (35 см)', 'multiplier': Decimal('1.2')},
            {'size': 'Средняя (30 см)', 'multiplier': Decimal('1.0')},
            {'size': 'Маленькая (25 см)', 'multiplier': Decimal('0.8')},
        ]
        
        created_sizes = []
        for size_data in sizes:
            size = PizzaSize.objects.create(**size_data)
            created_sizes.append(size)

        # Создаем категории
        categories = {
            'Классические': 'Традиционные итальянские пиццы',
            'Острые': 'Острые пиццы',
            'Вегетарианские': 'Пиццы без мяса'
        }
        
        created_categories = {}
        for name, desc in categories.items():
            cat = PizzaCategory.objects.create(name=name, description=desc)
            created_categories[name] = cat

        # Создаем аллергены
        allergens_data = {
            'Глютен': 'Содержится в тесте',
            'Лактоза': 'Содержится в сыре',
            'Яйца': 'Может содержаться в тесте',
        }
        created_allergens = {}
        for name, desc in allergens_data.items():
            allergen = Allergen.objects.create(name=name, description=desc)
            created_allergens[name] = allergen

        # Создаем ингредиенты
        ingredients_data = {
            'Моцарелла': {'description': 'Сыр моцарелла', 'is_vegetarian': True},
            'Томатный соус': {'description': 'Соус из томатов', 'is_vegetarian': True},
            # ...другие ингредиенты...
        }
        
        created_ingredients = {}
        for name, data in ingredients_data.items():
            ingredient = Ingredient.objects.create(
                name=name,
                description=data['description'],
                is_vegetarian=data['is_vegetarian']
            )
            created_ingredients[name] = ingredient

        # Создаем пиццы
        pizzas = [
            {
                'name': 'Маргарита',
                'category': 'Классические',
                'description': 'Классическая итальянская пицца с томатным соусом, сыром моцарелла и базиликом. Аллергены: глютен, лактоза.',
                'base_price': Decimal('500'),
                'is_vegan': True,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Базилик'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Пепперони',
                'category': 'Острые',
                'description': 'Острая пицца с пепперони и сыром моцарелла. Аллергены: глютен, лактоза.',
                'base_price': Decimal('600'),
                'is_vegan': False,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Пепперони'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Четыре сыра',
                'category': 'Классические',
                'description': 'Соус альфредо, моцарелла, пармезан, горгонзола, сыр с голубой плесенью',
                'base_price': Decimal('700'),
                'is_vegan': False,
                'sauce': 'Альфредо',
                'ingredients': ['Моцарелла', 'Пармезан', 'Горгонзола', 'Сыр с голубой плесенью'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Вегетарианская',
                'category': 'Вегетарианские',
                'description': 'Томатный соус, грибы, сладкий перец, красный лук, оливки, томаты черри',
                'base_price': Decimal('550'),
                'is_vegan': True,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Грибы', 'Сладкий перец', 'Красный лук', 'Оливки', 'Томаты черри'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Гавайская',
                'category': 'Классические',
                'description': 'Томатный соус, ветчина, ананасы, моцарелла',
                'base_price': Decimal('600'),
                'is_vegan': False,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Ветчина', 'Ананасы'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Дьябло',
                'category': 'Острые',
                'description': 'Острый томатный соус, салями, перец халапеньо, красный лук, моцарелла',
                'base_price': Decimal('650'),
                'is_vegan': False,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Салями', 'Перец халапеньо', 'Красный лук'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Грибная',
                'category': 'Вегетарианские',
                'description': 'Соус альфредо, шампиньоны, лесные грибы, трюфельное масло, моцарелла',
                'base_price': Decimal('680'),
                'is_vegan': True,
                'sauce': 'Альфредо',
                'ingredients': ['Моцарелла', 'Шампиньоны', 'Лесные грибы', 'Трюфельное масло'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Барбекю',
                'category': 'Классические',
                'description': 'Соус барбекю, куриное филе, бекон, красный лук, моцарелла',
                'base_price': Decimal('650'),
                'is_vegan': False,
                'sauce': 'Барбекю',
                'ingredients': ['Моцарелла', 'Соус барбекю', 'Куриное филе', 'Бекон', 'Красный лук'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Мексиканская',
                'category': 'Острые',
                'description': 'Томатный соус, говяжий фарш, перец халапеньо, кукуруза, фасоль, моцарелла',
                'base_price': Decimal('670'),
                'is_vegan': False,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Говяжий фарш', 'Перец халапеньо', 'Кукуруза', 'Фасоль'],
                'allergens': ['Глютен', 'Лактоза']
            },
            {
                'name': 'Средиземноморская',
                'category': 'Вегетарианские',
                'description': 'Томатный соус, артишоки, оливки, вяленые томаты, руккола, моцарелла',
                'base_price': Decimal('630'),
                'is_vegan': True,
                'sauce': 'Томатный',
                'ingredients': ['Моцарелла', 'Томатный соус', 'Артишоки', 'Оливки', 'Вяленые томаты', 'Руккола'],
                'allergens': ['Глютен', 'Лактоза']
            }
        ]

        for pizza_data in pizzas:
            # Создаем пиццу
            pizza = Pizza.objects.create(
                name=pizza_data['name'],
                description=pizza_data['description'],
                category=created_categories[pizza_data['category']],
                is_vegan=pizza_data['is_vegan'],
                sauce=pizza_data['sauce']
            )

            # Добавляем ингредиенты и аллергены
            existing_ingredients = []
            for ingredient_name in pizza_data['ingredients']:
                ingredient = created_ingredients.get(ingredient_name)
                if ingredient:
                    existing_ingredients.append(ingredient)

            pizza.ingredients.set(existing_ingredients)
            pizza.allergens.set([created_allergens[a] for a in pizza_data['allergens']])

            # Создаем цены для каждого размера
            for size in created_sizes:
                PizzaPricing.objects.create(
                    pizza=pizza,
                    size=size,
                    price=pizza_data['base_price'] * size.multiplier
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно обновлена'))
