# Generated by Django 4.0.4 on 2023-08-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_portfolio', '0018_alter_portfolio_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='instagram',
            field=models.URLField(default='https://www.instagram.com/qu_est.py/?igshid=OGQ5ZDc20Dk2ZA%3D%3D'),
            preserve_default=False,
        ),
    ]