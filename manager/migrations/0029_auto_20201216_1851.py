# Generated by Django 3.1.3 on 2020-12-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('manager', '0028_auto_20201212_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(db_index=True, help_text='Имя книги', max_length=50, verbose_name='название'),
        ),
    ]
