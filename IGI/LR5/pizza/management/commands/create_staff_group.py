from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Creates staff group with permissions'

    def handle(self, *args, **kwargs):
        staff_group, created = Group.objects.get_or_create(name='Staff')
        if created:
            permissions = [
                'view_pizza', 'add_pizza', 'change_pizza',
                'view_order', 'change_order',
                'view_customer',
                'view_courier', 'change_courier',
                'view_review'
            ]
            for perm_codename in permissions:
                perm = Permission.objects.get(codename=perm_codename)
                staff_group.permissions.add(perm)
