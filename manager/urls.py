from django.urls import path

from manager.views import MyPage, AddLikeComment, AddRate2Book, BookDetail, AddBook, comment_delete

from manager.views import LoginView, logout_user, AddComment, book_delete, BookUpdate, CommentUpdate, RegisterView
from manager.views import PegeGenre
urlpatterns =[
    path('add_like_comment/<int:comment_id>/<str:slug>/', AddLikeComment.as_view(), name="add-like"),
    path('add_rate_to_book/<str:slug>/<int:rate>/', AddRate2Book.as_view(), name='add-rate'),
    path('add_rate_to_book/<str:slug>/<int:rate>/<str:location>/',
         AddRate2Book.as_view(), name='add-rate-location'),
    path('add_book/', AddBook.as_view(), name='add-book'),
    path('add_comment/<str:slug>/', AddComment.as_view(), name='add-comment'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update_comment/<str:slug>/<int:comment_id>', CommentUpdate.as_view(), name='update-comment'),
    path('del_comment/<int:comment_id>/<str:slug>/', comment_delete, name="del-comment"),
    path('update_book/<str:slug>/', BookUpdate.as_view(), name="update-book"),
    path('del_book/<str:slug>/', book_delete, name="del-book"),
    path('page_genre/<str:genre>/', PegeGenre.as_view(), name="page-genre"),
    path('book_view_detail/<str:slug>/', BookDetail.as_view(), name="book-detail"),
    path('', MyPage.as_view(), name='the-main-page')

]

