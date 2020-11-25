from django.urls import path

from manager.views import hello, bui

urlpatterns =[
    path('hello/', hello),
    path('goodbye/', bui)

]

