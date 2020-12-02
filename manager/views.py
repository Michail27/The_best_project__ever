from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from manager.models import Book


def hello(request, name="filipp", digit =None):
    if digit is not None:
        return HttpResponse(f"digit is {digit}")
    return HttpResponse(f'Hello {name}')

def bui(request):
    return HttpResponse('Goodbye')
# Create your views here.

class MyPage(View):
    def get(self, request):
        context = {'books': Book.objects.all()}
        return render(request, 'index.html', context)