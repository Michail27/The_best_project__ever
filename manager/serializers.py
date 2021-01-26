from rest_framework.serializers import ModelSerializer
from manager.models import Comment, LikeCommentUser, Book


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LikeCommentUserSerializer(ModelSerializer):
    class Meta:
        model = LikeCommentUser
        fields = '__all__'


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'text']


