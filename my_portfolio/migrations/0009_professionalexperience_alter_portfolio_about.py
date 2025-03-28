# Generated by Django 4.0.4 on 2023-01-10 23:26

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_portfolio', '0008_alter_feedback_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('duration', models.CharField(help_text='start year - end year', max_length=30)),
                ('remote', models.BooleanField(default=True)),
                ('experience', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='about',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
