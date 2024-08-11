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
]