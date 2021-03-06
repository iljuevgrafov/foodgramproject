# Generated by Django 3.0.8 on 2021-01-17 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_auto_20210117_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoplist',
            name='recipes',
            field=models.ManyToManyField(related_name='inshoplist', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='shoplist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shoplist', to=settings.AUTH_USER_MODEL),
        ),
    ]
