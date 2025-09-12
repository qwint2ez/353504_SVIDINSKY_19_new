from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pizza.models import Pizza, Order, Review, Customer, Courier, Promo

class Command(BaseCommand):
    help = 'Create employee group with permissions'

    def handle(self, *args, **kwargs):
        # Создаем группу для сотрудников
        employee_group, created = Group.objects.get_or_create(name='Employees')
        
        # Список моделей, к которым нужен доступ
        models = [Pizza, Order, Review, Customer, Courier, Promo]
        
        # Добавляем все разрешения для этих моделей
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                employee_group.permissions.add(perm)
        
        self.stdout.write(self.style.SUCCESS('Successfully created employee group'))
