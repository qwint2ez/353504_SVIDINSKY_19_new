from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='image',
            field=models.ImageField(upload_to='pizzas/', null=True, blank=True, verbose_name='Изображение'),
        ),
    ]
