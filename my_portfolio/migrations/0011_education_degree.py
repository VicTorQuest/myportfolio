# Generated by Django 4.0.4 on 2023-01-11 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_portfolio', '0010_education_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='degree',
            field=models.CharField(default='University', max_length=100),
            preserve_default=False,
        ),
    ]