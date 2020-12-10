from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Book, LikeBookUser, Comment, LikeCommentUser


def hello(request, name="filipp", digit=None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f'Hello {name}')


def bui(request):
    return HttpResponse('Goodbye')


# class MyPage(View):
#     def get(self, request):
#         context = {}
#         comment_query = Comment.objects.annotate(count_like=Count('users_likes')).select_related('author')
#         comments = Prefetch('comments', comment_query)
#         books = Book.objects.prefetch_related('authors', comments)
#         context['books'] = books.annotate(count_like=Count('users_likes')), count_comment=Count("comments")
#         return render(request, 'index.html', context)

class MyPage(View):
    def get(self, request):
        context = {}
        comment_query = Comment.objects.annotate(count_like=Count('users_likes')).select_related('author')
        comments = Prefetch('comments', comment_query)
        books = Book.objects.prefetch_related('authors', comments)
        context['books'] = books
        context['rate'] = "3"
        return render(request, 'index.html', context)



class AddLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeBookUser.objects.create(user=request.user, book_id=id)
            # book = Book.objects.get(id=id)
            # book.likes += 1
            # book.save()
        return redirect("the-main-page")


class AddLikeComment(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeCommentUser.objects.create(user=request.user, comment_id=id)
        return redirect("the-main-page")


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
    def get(self, request, id, rate):
        return redirect('the-main-page')


class BookDetail(View):
    def get(self, request, id):
        comment_query = Comment.objects.annotate(count_like=Count("users_likes")).select_related("author")
        comments = Prefetch("comments", comment_query)
        book = Book.objects.prefetch_related('authors', comments).get(id=id)
        return render(request, "book_detail.html", {'book': book, 'rate': 2})
