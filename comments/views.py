from django.shortcuts import render
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from accounts.models import Account
from rest_framework import filters
from rest_framework import generics
from django.http import Http404
from . permissions import IsAuthorOrReadOnly
# Create your views here.

class PostCommentView(APIView):
    # permission_classes
    serializer_class = CommentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        # print(request.user)
        if serializer.is_valid():
            account = Account.objects.get(user=request.user)
            serializer.save(account=account)
            # print(account)
            return Response({'details': 'comment successfully'},status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAndDeleteCommentView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    def get_objects(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except(Comment.DoesNotExist):
            raise Http404

    def get(self, request, pk, format=None):
        comment = self.get_objects(pk)
        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = self.get_objects(pk)
        serializer = self.serializer_class(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        comment = self.get_objects(pk)
        comment.delete()
        return Response({'details': "comment deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class CommentForSpecificPost(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # print(request.user)
        post_id = request.query_params.get('post_id')
        if post_id:
            return queryset.filter(post = post_id)
        return queryset

# ak ta post e koto gula comment ase ta daker view
class TotalCommentForSinglePostView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [CommentForSpecificPost]