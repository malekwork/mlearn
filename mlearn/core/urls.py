from django.urls import path, include
from .views import SubscriptionListCreateView, CategoryListCreateView, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('', include(router.urls)),
]
