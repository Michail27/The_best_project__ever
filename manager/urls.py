
from django.urls import path
from django.views.decorators.cache import cache_page

from manager.oauth_viev import aouch_viev
from manager.views import MyPage, AddLikeComment, AddRate2Book, BookDetail, AddBook, comment_delete, ProfilUser
from manager.views import LoginView, logout_user, AddComment, book_delete, BookUpdate, CommentUpdate, RegisterView
from manager.views import PegeGenre
from manager.views_ajax import UpdateComment, delete_book_ajax, add_rate2book_ajax, AddLikeComments, CreateBook
from manager.views_ajax import add_comment_ajax, DeliteComment

urlpatterns =[
    path('add_like_comment/<int:comment_id>/<str:slug>/', AddLikeComment.as_view(), name="add-like"),
    path('add_like2comment_ajax/<int:pk>', AddLikeComments.as_view()),
    path('update_comment_ajax/<int:id>', UpdateComment.as_view()),
    path('add_rate_to_book/<str:slug>/<int:rate>/', AddRate2Book.as_view(), name='add-rate'),
    path('add_rate2book_ajax/', add_rate2book_ajax),
    path('add_rate_to_book/<str:slug>/<int:rate>/<str:location>/',
         AddRate2Book.as_view(), name='add-rate-location'),
    path('add_book/', AddBook.as_view(), name='add-book'),
    path('add_comment/<str:slug>/', AddComment.as_view(), name='add-comment'),
    path('add_comment_ajax/', add_comment_ajax, name='comment-ajax'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update_comment/<str:slug>/<int:comment_id>', CommentUpdate.as_view(), name='update-comment'),
    path('del_comment/<int:comment_id>/<str:slug>/', comment_delete, name="del-comment"),
    path('delete_comment_ajax/<int:id>', DeliteComment.as_view()),
    path('update_book/<str:slug>/', BookUpdate.as_view(), name="update-book"),
    path('del_book/<str:slug>/', book_delete, name="del-book"),
    path('delete_book_ajax/', delete_book_ajax),
    path('page_genre/<str:genre>/', PegeGenre.as_view(), name="page-genre"),
    path('profil_user/', ProfilUser.as_view(), name='profil'),
    path('book_view_detail/<str:slug>/', cache_page(10)(BookDetail.as_view()), name="book-detail"),
    path('callback_aouch/', aouch_viev, name='callback-aouch'),
    path('create_book_ajax/', CreateBook.as_view()),
    path('', MyPage.as_view(), name='the-main-page')

]
