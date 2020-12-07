from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    title = models.CharField(
        max_length=50,
        verbose_name='название',
        help_text='Имя книги'
    )
    data = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField()
    authors = models.ManyToManyField(User, related_name="books")
    # likes = models.PositiveIntegerField(default=0)
    likes1 = models.ManyToManyField(User, through='manager.LikeBookUser', related_name='liked_books')

    def __str__(self):
        return f"{self.title} - {self.id:}"


class LikeBookUser(models.Model):
    class Meta:
        unique_together = ('user', 'book')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_book_table')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='liked_user_table')

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeBookUser.objects.get(user=self.user, book=self.book).delete()


class Comment(models.Model):
    text = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes2 = models.ManyToManyField(User, through='manager.LikeCommentUser', related_name='liked_comments')


class LikeCommentUser(models.Model):
    class Meta:
        unique_together = ('user', 'comment')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comment_table')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='liked_user_comment_table')

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            LikeCommentUser.objects.get(user=self.user, comment=self.comment).delete()
