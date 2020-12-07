# Generated by Django 3.1.3 on 2020-12-06 03:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0012_auto_20201205_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeCommentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_user_comment_table', to='manager.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comment_table', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='likes2',
            field=models.ManyToManyField(related_name='liked_comments', through='manager.LikeCommentUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
