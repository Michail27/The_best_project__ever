from django.contrib import admin
from manager.models import Book, Comment


class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 2
    exclude = ['likes_for_comment']


class BookAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    readonly_fields = ['rate']
    exclude = ['count_rated_users', 'count_all_stars']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Book, BookAdmin)

