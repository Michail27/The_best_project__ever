from django.db.models import Prefetch, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from manager.models import Book, Comment, LikeCommentUser
from manager.models import LikeBookUser as RateBookUser


def hello(request, name="filipp", digit=None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f'Hello {name}')


def bui(request):
    return HttpResponse('Goodbye')

#
# class MyPage(View):
#     def get(self, request):
#         context = {}
#         comment_query = Comment.objects.annotate(count_like=Count('users_likes')).select_related('author')
#         comments = Prefetch('comments', comment_query)
#         books = Book.objects.prefetch_related('authors', comments)
#         context['books'] = books.annotate(count_like=Count('users_likes'))
#         return render(request, 'index.html', context)


class MyPage(View):
    def get(self, request):
        context = {}
        comment_query = Comment.objects.select_related('author')
        comments = Prefetch('comments', comment_query)
        context['books'] = Book.objects.prefetch_related('authors', comments)
        context['range'] = range(1, 6)
        return render(request, 'index.html', context)


class AddLikeComment(View):
    def get(self, request, slug, id, location=None):
        if request.user.is_authenticated:
            LikeCommentUser.objects.create(user=request.user, comment_id=id)
        if location is None:
            return redirect("the-main-page")
        return redirect("book-detail", slug=slug)


class DelComment(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            Comment.objects.get(id=id).delete()
        return redirect("the-main-page")


class DelBook(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            Book.objects.get(id=id).delete()
        return redirect("the-main-page")


class AddRate2Book(View):
    def get(self, request, slug, id, rate, location=None):
        if request.user.is_authenticated:
            RateBookUser.objects.create(user=request.user, book_id=id, rate=rate)
        if location is None:
            return redirect('the-main-page')
        return redirect("book-detail", slug=slug)


class BookDetail(View):
    def get(self, request, slug):
        context = {}
        comment_query = Comment.objects.select_related("author")
        comments = Prefetch("comments", comment_query)
        context['book'] = Book.objects.prefetch_related('authors', comments).get(slug=slug)
        context['range'] = range(1, 6)
        return render(request, "book_detail.html", context)



