from django.urls import path

from .views import send_otp_view, VerifyOTPTemplateView, RegisterTemplateView, LoginView, LogoutView
from .views import user_profile, change_password, user_update

urlpatterns = [
    path('send-otp/', send_otp_view, name='send-otp'),
    path('verify-otp/', VerifyOTPTemplateView.as_view(), name='verify-otp'),
    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', user_profile, name='profile'),
    path('update/', user_update, name='update'),
    path('change-password/', change_password, name='change-password'),
]
