from django.urls import path

from manager.views import hello, bui, MyPage, AddLike

urlpatterns =[
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('hello/', hello),
    path('goodbye/', bui),
    path('add_like/<int:id>/', AddLike.as_view(), name="add-like"),
    path('', MyPage.as_view(), name='the-main-page')


]

