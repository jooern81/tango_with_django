# Generated by Django 3.0.3 on 2020-08-23 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20200823_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=128, unique=True),
        ),
    ]
