from django.urls import path
from .views import index_view, send_otp, verify_otp, register, login

urlpatterns = [
    path('', index_view, name='index'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
