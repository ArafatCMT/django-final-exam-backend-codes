from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.PostUploadView.as_view()),
    path('detail/<int:pk>/', views.PostDetail.as_view()),
    path('all/', views.AllPostView.as_view())

]