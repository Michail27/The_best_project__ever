from django.urls import path

from manager.views import hello, bui, MyPage, AddLikeComment, DelComment, DelBook, AddRate2Book, BookDetail, AddBook
from manager.views import LoginView, logout_user, AddComment
urlpatterns =[
    path("hello/<int:digit>/", hello),
    path('hello/<str:name>/', hello),
    path('hello/', hello),
    path('goodbye/', bui),
    path('add_like_comment/<str:slug>/<int:comment_id>', AddLikeComment.as_view(), name="add-like-comment"),
    path('add_like_comment/<int:comment_id>/<str:slug>/<str:location>', AddLikeComment.as_view(), name="add-like-location"),
    path('del_book/<int:id>/', DelBook.as_view(), name="del-book"),
    path('del_comment/<int:id>/<str:slug>', DelComment.as_view(), name="del-comment"),
    path('add_rate_to_book/<str:slug>/<int:rate>/', AddRate2Book.as_view(), name='add-rate'),
    path('add_rate_to_book/<str:slug>/<int:rate>/<str:location>',
         AddRate2Book.as_view(), name='add-rate-location'),
    path('book_view_detail/<str:slug>', BookDetail.as_view(), name="book-detail"),
    path('add_book/', AddBook.as_view(), name='add-book'),
    path('add_comment/<str:slug>', AddComment.as_view(), name='add-comment'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('', MyPage.as_view(), name='the-main-page')


]

