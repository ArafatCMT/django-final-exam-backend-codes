from django.shortcuts import render
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from accounts.models import Account
from rest_framework import filters
from rest_framework import generics
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