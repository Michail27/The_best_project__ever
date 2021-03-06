# Generated by Django 3.1.3 on 2020-12-19 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0032_auto_20201217_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMPBook',
            fields=[
                ('title', models.CharField(db_index=True, help_text='Имя книги', max_length=50, verbose_name='название')),
                ('data', models.DateTimeField(auto_now_add=True, null=True)),
                ('text', models.TextField()),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('count_rated_users', models.PositiveIntegerField(default=0)),
                ('count_all_stars', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('authors', models.ManyToManyField(related_name='tmp_books', to=settings.AUTH_USER_MODEL)),
                ('users_likes', models.ManyToManyField(related_name='liked_tmp_books', through='manager.LikeBookUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
        migrations.DeleteModel(
            name='TestComment',
        ),
        migrations.DeleteModel(
            name='TestTale',
        ),
        migrations.AddField(
            model_name='comment',
            name='tmp_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='manager.tmpbook'),
        ),
        migrations.AddField(
            model_name='likebookuser',
            name='tmp_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_user_table', to='manager.tmpbook'),
        ),
    ]
