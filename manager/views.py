from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse('Hello world')

def bui(request):
    return HttpResponse('Goodbye')
# Create your views here.
