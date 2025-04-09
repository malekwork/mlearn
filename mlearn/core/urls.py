from django.urls import path, include
from .views import subscription_create, subscription_list, post_create, category_posts
from .views import category_create, category_list, post_detail, comment_create
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('subscriptions/', subscription_list, name='subscription_list'),
    path('subscriptions/create/', subscription_create, name='subscription_create'),
    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('category/<int:category_id>/posts/', category_posts, name='category_posts'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='create_post'),
    path('post/<int:post_id>/comment/', comment_create, name='comment_create'),
]
