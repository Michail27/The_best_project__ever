from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Book, LikeBookUser


def hello(request, name="filipp", digit =None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f'Hello {name}')

def bui(request):
    return HttpResponse('Goodbye')
# Create your views here.

class MyPage(View):
    def get(self, request):
        context = {}
        context['books'] = Book.objects.prefetch_related('authors', 'comments').annotate(count=Count('likes1'))

        return render(request, 'index.html', context)

class AddLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            LikeBookUser.objects.create(user=request.user, book_id=id)
            # book = Book.objects.get(id=id)
            # book.likes += 1
            # book.save()
        return redirect("the-main-page")