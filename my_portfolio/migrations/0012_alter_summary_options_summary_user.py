# Generated by Django 4.0.4 on 2023-01-11 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_portfolio', '0011_education_degree'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summary',
            options={'verbose_name_plural': 'Summary'},
        ),
        migrations.AddField(
            model_name='summary',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
