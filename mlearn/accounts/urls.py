from django.urls import path

from .views import SendOTPView, VerifyOTPView, RegisterView, LoginView, LogoutView, CheckLoginStatusView
from .views import UserProfileView, UserUpdateView, ChangePasswordView, PurchaseSubscriptionView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('is-authenticated/', CheckLoginStatusView.as_view(), name='is-authenticated'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('purchase-subscription/', PurchaseSubscriptionView.as_view(), name='purchase-subscription'),
]
