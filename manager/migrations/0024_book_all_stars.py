# Generated by Django 3.1.3 on 2020-12-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0023_auto_20201211_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='all_stars',
            field=models.PositiveIntegerField(default=0),
        ),
    ]