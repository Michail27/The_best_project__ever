from django.urls import path
from Aouth.views import MyPageButton, git_button

urlpatterns =[
    path('callback/', git_button, name='answer_git'),
    path('', MyPageButton.as_view(), name='button_git'),

]