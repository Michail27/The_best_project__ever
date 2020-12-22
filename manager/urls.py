from django.urls import path

from manager.views import MyPage, AddLikeComment, AddRate2Book, BookDetail, AddBook, comment_delete
from manager.views import LoginView, logout_user, AddComment, book_delete, BookUpdate, CommentUpdate
urlpatterns =[


    path('add_like_comment/<int:comment_id>/<str:slug>/', AddLikeComment.as_view(), name="add-like-location"),
    path('del_book/<str:slug>/', book_delete, name="del-book"),
    path('del_comment/<int:comment_id>/<str:slug>/', comment_delete, name="del-comment"),
    path('add_rate_to_book/<str:slug>/<int:rate>/', AddRate2Book.as_view(), name='add-rate'),
    path('add_rate_to_book/<str:slug>/<int:rate>/<str:location>/',
         AddRate2Book.as_view(), name='add-rate-location'),
    path('book_view_detail/<str:slug>/', BookDetail.as_view(), name="book-detail"),
    path('add_book/', AddBook.as_view(), name='add-book'),
    path('add_comment/<str:slug>/', AddComment.as_view(), name='add-comment'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('update_comment/<str:slug>/<int:comment_id>', CommentUpdate.as_view(), name='update-comment'),
    path('update_book/<str:slug>/', BookUpdate.as_view(), name="update-book"),
    path('', MyPage.as_view(), name='the-main-page')


]

