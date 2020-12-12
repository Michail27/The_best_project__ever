# Generated by Django 3.1.3 on 2020-12-11 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0022_auto_20201211_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='number_of_stars',
        ),
        migrations.CreateModel(
            name='RateBookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_stars', models.PositiveIntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_user_table', to='manager.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_book_table', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'book')},
            },
        ),
        migrations.AddField(
            model_name='book',
            name='users_rate',
            field=models.ManyToManyField(related_name='rate_books', through='manager.RateBookUser', to=settings.AUTH_USER_MODEL),
        ),
    ]