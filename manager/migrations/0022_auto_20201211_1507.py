# Generated by Django 3.1.3 on 2020-12-11 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_book_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='rating',
            new_name='number_of_stars',
        ),
        migrations.RemoveField(
            model_name='book',
            name='users_likes_for_rite',
        ),
        migrations.DeleteModel(
            name='RateBookUser',
        ),
    ]