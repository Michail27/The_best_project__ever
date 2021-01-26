from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from manager.forms import CommentForm
from manager.models import LikeCommentUser, Comment, Book
from manager.models import LikeBookUser as RateBookUser
from manager.permissions import IsAuthor
from manager.serializers import CommentSerializer, LikeCommentUserSerializer, BookSerializer


# def add_like2comment_ajax(request, comment_id):
#     if request.user.is_authenticated:
#         LikeCommentUser.objects.create(user=request.user, comment_id=comment_id)
#         comment = Comment.objects.get(id=comment_id)
#         count_likes = comment.likes_for_comment
#         return JsonResponse({'likes': count_likes}, status=status.HTTP_201_CREATED)
#     return JsonResponse({'error': 'user is not authenticated '}, status=status.HTTP_401_UNAUTHORIZED)
class AddLikeComments(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeCommentUserSerializer
    queryset = LikeCommentUser.objects.all()

    def get_object(self):
        user = self.request.user
        comment_id = self.kwargs['pk']
        query_set = LikeCommentUser.objects.filter(user=user, comment_id=comment_id)
        if query_set.exists():
            return query_set.first()

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            LikeCommentUser.objects.create(user=request.user, comment_id=self.kwargs['pk'])
        else:
            obj.delete()
        comment = LikeCommentUser.objects.filter(comment_id=self.kwargs['pk'])
        count_likes = comment.count()
        return Response({'likes': count_likes}, status=status.HTTP_201_CREATED)


class CreateBook(CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer


class UpdateComment(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    lookup_field = 'id'
    queryset = Comment.objects.all()

# def delete_comment_ajax(request, comment_id):
#     if request.user.is_authenticated:
#         comment = Comment.objects.get(id=comment_id)
#         if request.user == comment.author:
#             comment.delete()
#             return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
#         return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)
#     return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)


# class DeliteComment(APIView):
#     def delete(self, request, comment_id):
#         if request.user.is_authenticated:
#             comment = Comment.objects.get(id=comment_id)
#             if request.user == comment.author:
#                 comment.delete()
#                 return Response({}, status=status.HTTP_204_NO_CONTENT)
#             return Response({}, status=status.HTTP_403_FORBIDDEN)
#         return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class DeliteComment(DestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    lookup_field = 'id'
    queryset = Comment.objects.all()


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




