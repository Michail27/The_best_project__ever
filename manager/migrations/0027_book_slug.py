# Generated by Django 3.1.3 on 2020-12-12 09:07

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('manager', '0026_auto_20201212_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
