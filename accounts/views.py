from django.shortcuts import render,redirect
from rest_framework.views import APIView
from accounts.models import Account, Friends,FriendRequest
from accounts import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.http import Http404
from accounts.permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters

# Create your views here.
class RegistrationView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            # print(user)
            # print(request.user)

            # confirmation mail ta ke strong korar jonno token and uid user korta ci 
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = f"https://net-book.onrender.com/accounts/verify/{uid}/{token}"

            email_subject = "Verify Your Account"
            email_body = render_to_string('verification_mail.html', {'verification_link': verification_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your email for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
def is_active(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid) # decode korar por jei uid ta pelam ei uid ta kon user er primary_key oi user ta ke get kortaci
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        print(user)
        user.is_active = True
        user.save()
        return redirect('https://arafatcmt.github.io/django-final-exam-frontend-codes/login.html')
    return redirect('register')


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # print(username, password)

            user = authenticate(username=username, password=password)
            # print(user)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                # print('get',token)

                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)


class UserLogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # print('logout',request.user)
        # request.user.auth_token.delete()
        logout(request)
        return Response({'details': 'logout successfully'})
        
        
class EditProfileView(APIView):
    # permission_classes = [IsAuthorOrReadOnly]
    serializer_class = serializers.ProfileSerializer

    def get_objects(self, pk):
        try:
            return Account.objects.get(id=pk)
        except(Account.DoesNotExist):
            raise Http404 
        
    def get(self, request, pk, format=None):
        # print(request.user)
        account = self.get_objects(pk)
        serializer = self.serializer_class(account)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        # print(request.user)
        account = self.get_objects(pk)
        serializer = self.serializer_class(account, data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FindUserApiView(APIView):
    serializer_class = serializers.UserSerializer

    def get_objects(self, pk):
        try:
            return User.objects.get(id=pk)
        except(User.DoesNotExist):
            raise Http404 
        
    def get(self, request, pk, format=None):
        # print(request.user)
        account = self.get_objects(pk)
        serializer = self.serializer_class(account)
        return Response(serializer.data)

class AllProfileView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = serializers.ProfileSerializer

# start friend request views
class FriendRequestAPIView(APIView):#
      serializer_class = serializers.FriendRequestSerializer

      def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # print(serializer.validated_data['receiver'])
            account = Account.objects.get(user=request.user)
            # print(serializer.validated_data['sender'])
            serializer.save(sender=account)
            return Response({'details': 'request successfully'},status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class AcceptFriendRequestView(APIView):#
    serializer_class = serializers.FriendSerializer

    def get_objects(self, sender_id, receiver_id):
        queryset = FriendRequest.objects.filter(sender_id = sender_id)

        try:
            return queryset.get(receiver_id = receiver_id)
        except(FriendRequest.DoesNotExist):
            return None
        
    def get(self, request, sender_id, receiver_id, is_accept, format=None):
        object = self.get_objects(sender_id, receiver_id)

        if object:
            if is_accept == 1:
                sender_account = Account.objects.get(id = object.sender.id)
                recever_receiver = Account.objects.get(id = object.receiver.id)
                friend = Friends.objects.create(receiver_account=recever_receiver, sender_account=sender_account)
                
                friend.save()
                
                object = FriendRequest.objects.get(id=object.id)
                object.delete()

            if is_accept == 0:
                object = FriendRequest.objects.get(id=object.id)
                object.delete()
                print('deleted')
        else:
            print(object)
        serializer = serializers.FriendRequestSerializer(object)
        return Response(serializer.data)
    
class ShowFriendPart_1(filters.BaseFilterBackend):#
    def filter_queryset(self, request, queryset, view):
        account_id = request.query_params.get('account_id')
        if account_id:
            return queryset.filter(sender_account = account_id)
        return queryset
    
class ShowFriendPart_2(filters.BaseFilterBackend):#
    def filter_queryset(self, request, queryset, view):
        account_id = request.query_params.get('account_id')
        if account_id:
            return queryset.filter(receiver_account = account_id)
        return queryset
    
class FriendSendRequestAccept(generics.ListAPIView):#
    queryset = Friends.objects.all()
    serializer_class = serializers.FriendSerializer
    filter_backends = [ShowFriendPart_1]

class FriendReceiveRequestAccept(generics.ListAPIView):#
    queryset = Friends.objects.all()
    serializer_class = serializers.FriendSerializer
    filter_backends = [ShowFriendPart_2]

class UnfriendView(APIView):

    def get_objects(self, account_id, id):
        queryset = Friends.objects.filter(receiver_account=id)
        try:
            return queryset.get(sender_account = account_id)
        except(Friends.DoesNotExist):
            friend = Friends.objects.filter(sender_account=id)
            try:
                return friend.get(receiver_account=account_id)
            except(Friends.DoesNotExist):
                return None

    def get(self, request, id, format=None):
        account = Account.objects.get(user = request.user)
        friend = self.get_objects(account.id, id)
        if(friend):
            # print(friend.id, friend.receiver_account, friend.sender_account)
            friend.delete()
        serializer = serializers.FriendSerializer(friend)
        return Response(serializer.data)
    
class IsFriendView(APIView):
    # permission_classes = permissions.IsAuthenticatedOrReadOnly
    def get_objects(self, account_id, id):
        queryset = Friends.objects.filter(receiver_account=id)
        try:
            return queryset.get(sender_account = account_id)
        except(Friends.DoesNotExist):
            friend = Friends.objects.filter(sender_account=id)
            try:
                return friend.get(receiver_account=account_id)
            except(Friends.DoesNotExist):
                return None
            
    def get(self, request, id_, id, format=None):
        
        account = Account.objects.get(id = id_)
        friend = self.get_objects(account.id, id)
        serializer = serializers.FriendSerializer(friend)
        return Response(serializer.data)
    
# class SendRequest(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         account_id = request.query_params.get('account_id')
#         if account_id:
#             return queryset.filter(sender = account_id)
#         return queryset
    
class receiveRequest(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        account_id = request.query_params.get('account_id')
        if account_id:
            return queryset.filter(receiver = account_id)
        return queryset

class SendRequestView(APIView):
    # queryset = FriendRequest.objects.all()
    # serializer_class = serializers.FriendRequestSerializer
    # filter_backends = [SendRequest]
    def get_objects(self, account_id, id):
        queryset = FriendRequest.objects.filter(receiver=id)
        try:
            return queryset.get(sender = account_id)
        except(FriendRequest.DoesNotExist):
            return None
        
    def get(self, request, id_, id, format=None):
        
        account = Account.objects.get(id = id_)
        friend_request = self.get_objects(account.id, id)
        serializer = serializers.FriendRequestSerializer(friend_request)
        return Response(serializer.data)

class ReceiveRequestView(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    filter_backends = [receiveRequest]





        