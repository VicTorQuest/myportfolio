# Generated by Django 4.0.4 on 2023-01-11 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_portfolio', '0016_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
