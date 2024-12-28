from django.urls import path 
from . import views

urlpatterns = [
    path('auth/login/', views.user_login),
    path('auth/register/', views.user_register),
    path('post/<int:pk>/', views.get_post),
    path('post/create/', views.create_post),
    path('profile/create/', views.create_profile),
    path('profile/<str:username>/', views.view_profile),
    path('like/<str:pk>/', views.like_post),
    path('get-post-likes/<str:pk>/', views.get_post_likes),
    path('post/<str:post_id>/add-comment/', views.add_comment),
    path('follow/<str:username>/', views.follow_user),
    path('post/<str:post_id>/view-comment/', views.get_post_comments),
    path('feed/', views.feed),
]
