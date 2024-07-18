from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from likes.serializers import LikeSerializer
from likes.models import Like
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters 
from accounts.models import Account
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class LikeView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_objects(self, request, post):
        try:
            likes = Like.objects.filter(post=post) # ak ta post e joto gula like ase sob gula array akare likes er moddhe asce
        except(Like.DoesNotExist):
            likes = None
        
        if likes:
            for like in likes:
                if request.user == like.account.user: # check kortaci user age ei post e like dece ki na
                    return like.id
            return None

    def post(self, request, format=None):
        print('r',request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            post = serializer.validated_data['post']
            print(post)
            id = self.get_objects(self.request, post)
            # print(ans)
            if id is None:
                # user er like ta save hocca 
                # print(id)
                account = Account.objects.get(user=request.user)
                print('a',account)
                serializer.save(account=account)
            else:
                # user jodi akta post already like deye thake tobe se jodi second time like dete jai tobe oi like dislike hoi e jabe
                like = Like.objects.get(id=id)
                like.delete()
                # print(like.post.account.user.username, like.user.username)
            return Response({'details': 'like successfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LikeForSpecificPost(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_id = request.query_params.get('post_id')
        if post_id:
            return queryset.filter(post = post_id)
        return queryset

# ak ta post koto gula like ase ta dakar view
class ShowLikeView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [LikeForSpecificPost]
