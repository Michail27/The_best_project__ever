from django.http import JsonResponse, HttpResponse
from rest_framework import status

from manager.forms import CommentForm
from manager.models import LikeCommentUser, Comment, Book
from manager.models import LikeBookUser as RateBookUser


def add_like2comment_ajax(request):
    if request.user.is_authenticated:
        comment_id = request.GET.get('comment_id')
        LikeCommentUser.objects.create(user=request.user, comment_id=comment_id)
        comment = Comment.objects.get(id=comment_id)
        count_likes = comment.likes_for_comment
        return JsonResponse({'likes': count_likes}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'user is not authenticated '}, status=status.HTTP_401_UNAUTHORIZED)


def delete_comment_ajax(request):
    if request.user.is_authenticated:
        comment_id = request.GET.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)


def delete_book_ajax(request):
    if request.user.is_authenticated:
        book_slug = request.GET.get('book_slug')
        book = Book.objects.get(slug=book_slug)
        if request.user in book.authors.all():
            book.delete()
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({book}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)


def add_rate2book_ajax(request):
    if request.user.is_authenticated:
        book_slug = request.GET.get('book_slug')
        rate = request.GET.get('rate')
        RateBookUser.objects.create(user=request.user, book_id=book_slug, rate=int(rate))
        book = Book.objects.get(slug=book_slug)
        count_rate = book.rate
        return JsonResponse({'rate': count_rate}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'user is not authenticated '}, status=status.HTTP_401_UNAUTHORIZED)


def add_comment_ajax(request):
    if request.user.is_authenticated :
        book_slug = request.POST.get('book_slug')
        new_comment = request.POST.get('new_comment')
        if new_comment:
            Comment.objects.create(author_id=request.user.id, book_id=book_slug, text=new_comment)
        return JsonResponse({'text': new_comment}, status=status.HTTP_201_CREATED)




