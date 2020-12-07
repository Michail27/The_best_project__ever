from django.contrib import admin
from manager.models import Book, Comment


class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 2


class BookAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]


admin.site.register(Book, BookAdmin)

