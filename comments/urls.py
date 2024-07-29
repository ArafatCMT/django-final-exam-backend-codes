from django.urls import path, include
from . import views

urlpatterns = [
    path('post/', views.PostCommentView.as_view()),
    path('list/', views.TotalCommentForSinglePostView.as_view()),
    path('detail/<int:pk>/', views.UpdateAndDeleteCommentView.as_view()),
]