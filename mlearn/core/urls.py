from django.urls import path, include
from .views import SubscriptionListCreateView, CategoryListCreateView, PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('', include(router.urls)),
]
