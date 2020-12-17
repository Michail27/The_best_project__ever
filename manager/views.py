from django.contrib.auth import login, logout
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

from manager.forms import BookForm, CustomAuthenticationForm
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
        context['form'] = BookForm()

        return render(request, 'index.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {'form': CustomAuthenticationForm()})

    def post(self, request):
        user = CustomAuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
        return redirect('the-main-page')


def logout_user(request):
    logout(request)
    return redirect('the-main-page')


class AddLikeComment(View):
    def get(self, request, slug, comment_id, location=None):
        if request.user.is_authenticated:
            LikeCommentUser.objects.create(user=request.user, comment_id=comment_id)
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
    def get(self, request, slug, rate, location=None):
        if request.user.is_authenticated:
            RateBookUser.objects.create(user=request.user, book=Book.objects.get(slug=slug), rate=rate)
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


class AddBook(View):
    def post(self, request):
        if request.user.is_authenticated:
            bf = BookForm(data=request.POST)
            book = bf.save(commit=True)
            book.authors.add(request.user)
            book.save()

            # book = Book.objects.create(
            #     title=request.POST['title'],
            #     text=request.POST['text'],
            # )
            # book.authors.add(request.user)
            # book.save()
        return redirect('the-main-page')

