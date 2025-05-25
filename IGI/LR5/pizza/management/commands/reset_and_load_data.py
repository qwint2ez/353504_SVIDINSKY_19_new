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

        # Создаем ингредиенты
        ingredients_data = {
            'Моцарелла': {'description': 'Сыр моцарелла', 'is_vegetarian': True},
            'Пармезан': {'description': 'Твердый сыр', 'is_vegetarian': True},
            'Горгонзола': {'description': 'Голубой сыр', 'is_vegetarian': True},
            'Сыр с голубой плесенью': {'description': 'Голубой сыр', 'is_vegetarian': True},
            'Томатный соус': {'description': 'Соус из томатов', 'is_vegetarian': True},
            'Соус альфредо': {'description': 'Сливочный соус', 'is_vegetarian': True},
            'Соус барбекю': {'description': 'Острый соус барбекю', 'is_vegetarian': True},
            'Острый томатный соус': {'description': 'Острый соус из томатов', 'is_vegetarian': True},
            'Пепперони': {'description': 'Острая салями', 'is_vegetarian': False},
            'Салями': {'description': 'Острая колбаса', 'is_vegetarian': False},
            'Грибы': {'description': 'Шампиньоны', 'is_vegetarian': True},
            'Шампиньоны': {'description': 'Грибы', 'is_vegetarian': True},
            'Лесные грибы': {'description': 'Ассорти грибов', 'is_vegetarian': True},
            'Ветчина': {'description': 'Свиная ветчина', 'is_vegetarian': False},
            'Говяжий фарш': {'description': 'Говядина', 'is_vegetarian': False},
            'Куриное филе': {'description': 'Курица', 'is_vegetarian': False},
            'Ананас': {'description': 'Консервированный ананас', 'is_vegetarian': True},
            'Перец халапеньо': {'description': 'Острый перец', 'is_vegetarian': True},
            'Сладкий перец': {'description': 'Болгарский перец', 'is_vegetarian': True},
            'Красный лук': {'description': 'Лук', 'is_vegetarian': True},
            'Оливки': {'description': 'Маслины', 'is_vegetarian': True},
            'Бекон': {'description': 'Копченый бекон', 'is_vegetarian': False},
            'Томаты': {'description': 'Свежие томаты', 'is_vegetarian': True},
            'Томаты черри': {'description': 'Мелкие томаты', 'is_vegetarian': True},
            'Вяленые томаты': {'description': 'Сушеные томаты', 'is_vegetarian': True},
            'Базилик': {'description': 'Свежий базилик', 'is_vegetarian': True},
            'Артишоки': {'description': 'Артишоки', 'is_vegetarian': True},
            'Руккола': {'description': 'Салат руккола', 'is_vegetarian': True},
            'Кукуруза': {'description': 'Сладкая кукуруза', 'is_vegetarian': True},
            'Фасоль': {'description': 'Красная фасоль', 'is_vegetarian': True},
            'Трюфельное масло': {'description': 'Масло с трюфелем', 'is_vegetarian': True}
        }

        created_ingredients = {}
        for name, data in ingredients_data.items():
            ingredient = Ingredient.objects.create(
                name=name,
                description=data['description'],
                is_vegetarian=data['is_vegetarian']
            )
            created_ingredients[name] = ingredient

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

        # Создаем пиццы с их ингредиентами
        pizzas = [
            {
                'name': 'Маргарита',
                'category': 'Классические',
                'description': 'Классическая итальянская пицца с томатным соусом и сыром',
                'price': Decimal('500'),
                'is_vegan': True,
                'ingredients': ['Моцарелла', 'Томатный соус', 'Базилик']
            },
            {
                'name': 'Пепперони',
                'category': 'Острые',
                'description': 'Острая пицца с пепперони',
                'price': Decimal('600'),
                'is_vegan': False,
                'ingredients': ['Моцарелла', 'Томатный соус', 'Пепперони']
            },
            {
                'name': 'Четыре сыра',
                'category': 'Классические',
                'description': 'Соус альфредо, моцарелла, пармезан, горгонзола, сыр с голубой плесенью',
                'price': Decimal('700'),
                'is_vegan': False,
                'ingredients': ['Моцарелла', 'Пармезан', 'Горгонзола', 'Сыр с голубой плесенью', 'Соус альфредо'],
                'allergens': ['Глютен', 'Лактоза'],
                'sauce': 'Альфредо'
            },
            {
                'name': 'Вегетарианская',
                'category': 'Вегетарианские',
                'description': 'Томатный соус, грибы, сладкий перец, красный лук, оливки, томаты черри',
                'price': Decimal('550'),
                'is_vegan': True,
                'ingredients': ['Томатный соус', 'Грибы', 'Сладкий перец', 'Красный лук', 'Оливки', 'Томаты черри'],
                'allergens': ['Глютен'],
                'sauce': 'Томатный'
            },
            {
                'name': 'Гавайская',
                'category': 'Классические',
                'description': 'Томатный соус, ветчина, ананасы, моцарелла',
                'price': Decimal('600'),
                'is_vegan': False,
                'ingredients': ['Томатный соус', 'Ветчина', 'Ананас', 'Моцарелла'],
                'allergens': ['Глютен', 'Лактоза'],
                'sauce': 'Томатный'
            },
            {
                'name': 'Дьябло',
                'category': 'Острые',
                'description': 'Острый томатный соус, салями, перец халапеньо, красный лук, моцарелла',
                'price': Decimal('650'),
                'is_vegan': False,
                'ingredients': ['Салями', 'Перец халапеньо', 'Красный лук', 'Моцарелла', 'Острый томатный соус'],
                'allergens': ['Глютен', 'Лактоза'],
                'sauce': 'Томатный'
            },
            {
                'name': 'Грибная',
                'category': 'Вегетарианские',
                'description': 'Соус альфредо, шампиньоны, лесные грибы, трюфельное масло, моцарелла',
                'price': Decimal('680'),
                'is_vegan': True,
                'ingredients': ['Соус альфредо', 'Шампиньоны', 'Лесные грибы', 'Трюфельное масло', 'Моцарелла'],
                'allergens': ['Глютен'],
                'sauce': 'Альфредо'
            },
            {
                'name': 'Барбекю',
                'category': 'Классические',
                'description': 'Соус барбекю, куриное филе, бекон, красный лук, моцарелла',
                'price': Decimal('650'),
                'is_vegan': False,
                'ingredients': ['Куриное филе', 'Бекон', 'Красный лук', 'Моцарелла', 'Соус барбекю'],
                'allergens': ['Глютен', 'Лактоза'],
                'sauce': 'Барбекю'
            },
            {
                'name': 'Мексиканская',
                'category': 'Острые',
                'description': 'Томатный соус, говяжий фарш, перец халапеньо, кукуруза, фасоль, моцарелла',
                'price': Decimal('670'),
                'is_vegan': False,
                'ingredients': ['Говяжий фарш', 'Перец халапеньо', 'Кукуруза', 'Фасоль', 'Моцарелла', 'Томатный соус'],
                'allergens': ['Глютен', 'Лактоза'],
                'sauce': 'Томатный'
            },
            {
                'name': 'Средиземноморская',
                'category': 'Вегетарианские',
                'description': 'Томатный соус, артишоки, оливки, вяленые томаты, руккола, моцарелла',
                'price': Decimal('630'),
                'is_vegan': True,
                'ingredients': ['Томатный соус', 'Артишоки', 'Оливки', 'Вяленые томаты', 'Руккола', 'Моцарелла'],
                'allergens': ['Глютен'],
                'sauce': 'Томатный'
            }
        ]

        # Создаем пиццы
        for pizza_data in pizzas:
            # Создаем пиццу
            pizza = Pizza.objects.create(
                name=pizza_data['name'],
                description=pizza_data['description'],
                category=created_categories[pizza_data['category']],
                is_vegan=pizza_data['is_vegan'],
                price=pizza_data['price']  # базовая цена
            )

            # Добавляем ингредиенты
            for ingredient_name in pizza_data['ingredients']:
                pizza.ingredients.add(created_ingredients[ingredient_name])

            # Создаем цены для каждого размера
            for size in created_sizes:
                PizzaPricing.objects.create(
                    pizza=pizza,
                    size=size,
                    price=pizza_data['price'] * size.multiplier
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно обновлена'))
