# Generated by Django 3.1.3 on 2020-12-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_comment_likes_for_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number_of_stars',
            field=models.PositiveIntegerField(default=0),
        ),
    ]