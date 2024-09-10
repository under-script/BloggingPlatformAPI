from django.urls import path

from api import views

urlpatterns = [
    # code omitted for brevity
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/detail/<int:pk>/', views.PostDetailAPIView.as_view()),
    path('posts/create/', views.PostCreateAPIView.as_view()),
    path('posts/update/<int:pk>/', views.PostUpdateAPIView.as_view()),
    path('posts/delete/<int:pk>/', views.PostDeleteAPIView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/detail/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('categories/create/', views.CategoryCreateAPIView.as_view()),
    path('categories/update/<int:pk>/', views.CategoryUpdateAPIView.as_view()),
    path('categories/delete/<int:pk>/', views.CategoryDeleteAPIView.as_view()),
]