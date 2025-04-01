from django.urls import path

from .views import SendOTPView, VerifyOTPView, RegisterView, LoginView, LogoutView, CheckLoginStatusView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('is-authenticated/', CheckLoginStatusView.as_view(), name='is-authenticated'),
]
