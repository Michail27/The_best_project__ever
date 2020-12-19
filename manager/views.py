from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from django.db.models import Prefetch, OuterRef, Exists

from django.shortcuts import render, redirect
from django.views import View


from manager.forms import BookForm, CustomAuthenticationForm, CommentForm
from manager.models import Book, Comment, LikeCommentUser
from manager.models import LikeBookUser as RateBookUser


class MyPage(View):
    def get(self, request):
        context = {}
        books = Book.objects.prefetch_related('authors')
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(books=OuterRef('pk'), id=request.user.id))
            books = books.annotate(is_owner=is_owner)
        context['books'] = books.order_by('-rate', 'data')
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
    def get(self, request, id, slug):
        if request.user.is_authenticated:
            Comment.objects.get(id=id).delete()
        return redirect("book-detail", slug=slug)


def book_delete(request, slug):
    if request.user.is_authenticated:
        book = Book.objects.get(slug=slug)
        if request.user in book.authors.all():
            book.delete()
            return redirect("the-main-page")


class AddRate2Book(View):
    def get(self, request, slug, rate, location=None):
        if request.user.is_authenticated:
            RateBookUser.objects.create(user=request.user, book_id=slug, rate=rate)
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
        context['form'] = CommentForm()

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


# class AddComment2(View):
#     def post(self, request, slug):
#         if request.user.is_authenticated:
#         #     book = Book.objects.get(slug=slug)
#         #     comment = book.comments.create(
#         #         text=request.POST['text'],
#         #         author=request.user
#         #     )
#         #     comment.save()
#         # return redirect("book-detail", slug=slug)


class AddComment(View):
    def post(self, request, slug):
        if request.user.is_authenticated:
            cf = CommentForm(data=request.POST)
            comment = cf.save(commit=False)
            comment.author = request.user
            book_id = Book.objects.get(slug=slug).id
            comment.book_id = book_id
            comment.save()
        return redirect("book-detail", slug=slug)


class BookUpdate(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                form = BookForm(instance=book)
                return render(request, 'update_book.html', {'form': form, 'slug': book.slug})
        return redirect('the-main-page')

    def post(self, request, slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=slug)
            if request.user in book.authors.all():
                bf = BookForm(instance=book, data=request.POST)
                if bf.is_valid():
                    bf.save(commit=True)
        return redirect('the-main-page')

