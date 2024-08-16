from django.urls import path, include
from accounts import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('verify/<uid64>/<token>/', views.is_active),
    path('profile/<int:pk>/', views.EditProfileView.as_view()),
    path('profile/', views.AllProfileView.as_view()),
    path('user/<int:pk>/', views.FindUserApiView.as_view()),

    path('friend/request/', views.FriendRequestAPIView.as_view()),#
    path('accept/<int:sender_id>/<int:receiver_id>/<int:is_accept>/', views.AcceptFriendRequestView.as_view()),#
    path('send/accept/', views.FriendSendRequestAccept.as_view()),#
    path('receive/accept/', views.FriendReceiveRequestAccept.as_view()),#
    path('unfriend/<int:id>/', views.UnfriendView.as_view()),#
    path('friend/<int:id_>/<int:id>/', views.IsFriendView.as_view()),#
    path('send/request/<int:id_>/<int:id>/', views.SendRequestView.as_view()),#
    path('receive/request/', views.ReceiveRequestView.as_view()),#
]