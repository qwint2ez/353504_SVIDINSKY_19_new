from django.core.management.base import BaseCommand
import os
import shutil

class Command(BaseCommand):
    help = 'Reset the database completely by removing the db.sqlite3 file and recreating migrations'

    def handle(self, *args, **options):
        self.stdout.write('Removing db.sqlite3...')
        db_path = 'db.sqlite3'
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS('Database file removed'))
        
        migrations_dir = os.path.join('pizza', 'migrations')
        self.stdout.write(f'Backing up migrations from {migrations_dir}...')
        
        # Backup migrations
        backup_dir = os.path.join(migrations_dir, 'backup')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Move all migration files except __init__.py to backup
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                src = os.path.join(migrations_dir, file)
                dst = os.path.join(backup_dir, file)
                shutil.move(src, dst)
                self.stdout.write(f'Backed up {file}')
        
        self.stdout.write(self.style.SUCCESS('All set! Now run:'))
        self.stdout.write('python manage.py makemigrations')
        self.stdout.write('python manage.py migrate')
        self.stdout.write('python manage.py reset_and_load_data')
