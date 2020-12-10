from django.core.management.base import BaseCommand
from django.db.models import Count

from manager.models import Book, Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        book = Book.objects.annotate(count_like=Count('users_likes'))
        # print([(i.likes, i.count_like) for i in book])
        # Book.objects.update(likes=45)
        for b in book:
            b.likes = b.count_like
        Book.objects.bulk_update(book, ['likes'])

    def handle2(self, *args, **options):
        comments = Comment.objects.annotate(count_like=Count('users_likes'))
        # print([(i.likes_for_comment, i.count_like) for i in comments])
        # Comment.objects.update(likes=45)
        for com in comments:
            com.likes_for_comment = com.count_like
        Comment.objects.bulk_update(comments, ['likes_for_comment'])




