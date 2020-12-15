from django.urls import path

from manager.views import hello, bui, MyPage, AddLikeComment, DelComment, DelBook, AddRate2Book, BookDetail

urlpatterns =[
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('hello/', hello),
    path('goodbye/', bui),
    path('add_like_comment/<int:id>/<str:slug>', AddLikeComment.as_view(), name="add-like-comment"),
    path('add_like_comment/<str:slug>/<int:id>/<str:location>', AddLikeComment.as_view(), name="add-like-location"),
    path('del_book/<int:id>/', DelBook.as_view(), name="del-book"),
    path('del_comment/<int:id>/', DelComment.as_view(), name="del-comment"),
    path('add_rate_to_book/<int:id>/<int:rate>/<str:slug>', AddRate2Book.as_view(), name='add-rate'),
    path('add_rate_to_book/<str:slug>/<int:id>/<int:rate>/<str:location>',
         AddRate2Book.as_view(), name='add-rate-location'),
    path('book_view_detail/<str:slug>', BookDetail.as_view(), name="book-detail"),
    path('', MyPage.as_view(), name='the-main-page')


]

