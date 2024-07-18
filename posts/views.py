from django.shortcuts import render
from rest_framework.views import APIView
from posts import serializers
from accounts.models import Account
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from django.http import Http404
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . permissions import IsAuthorOrReadOnly
# Create your views here.

class PostUploadView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer

    def get_objects(self, user):
        acccount = Account.objects.get(user=user)
        return acccount
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        
        print('add post',request.user)
        if serializer.is_valid():
            # print(serializer.validated_data['image_url'])
            account = self.get_objects(request.user)
            print(account.user)
            serializer.save(account=account)
            return Response({'details': 'post added successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDetail(APIView):
    # permission_classes = [IsAuthorOrReadOnly]
    serializer_class = serializers.PostSerializer

    def get_objects(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except(Post.DoesNotExist):
            raise Http404
        
    def get(self, request, pk, format=None):
        print(request.user)
        post = self.get_objects(pk)
        # serializer = self.serializer_class(post)
        serializer = serializers.PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        print('edit by',request.user)
        post = self.get_objects(pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = self.get_objects(pk)
        post.delete()
        return Response({'details': "post deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class PostForSpecificUser(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # print('all post', request.user)
        account_id = request.query_params.get('account_id')
        # print(account_id)
        if account_id:
            return queryset.filter(account = account_id)
        return queryset

class AllPostView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [PostForSpecificUser]


