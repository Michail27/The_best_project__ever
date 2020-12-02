from django.urls import path

from manager.views import hello, bui, MyPage

urlpatterns =[
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('hello/', hello),
    path('goodbye/', bui),
    path('', MyPage.as_view(), name='the-main-page')

]

