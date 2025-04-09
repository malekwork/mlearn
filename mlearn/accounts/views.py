import random
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions
from django.contrib.auth import update_session_auth_hash
from .models import Subscription
from .forms import ChangePasswordForm, UserUpdateForm

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


User = get_user_model()

otp_storage = {}  # Temporary storage for OTPs


def send_otp_view(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        if not mobile:
            return render(request, "frontend/send_otp.html", {"error": "Mobile number is required."})
        
        otp = random.randint(100000, 999999)
        otp_storage[mobile] = otp
        print(f"OTP for {mobile}: {otp}")

        request.session['mobile'] = mobile
        return redirect(reverse("verify-otp"))

    return render(request, "frontend/send_otp.html")


class VerifyOTPTemplateView(View):
    def get(self, request):
        return render(request, "frontend/verify_otp.html")

    def post(self, request):
        mobile = request.session.get("mobile")  
        entered_otp = request.POST.get("otp")

        if mobile is None or entered_otp is None:
            return render(request, "frontend/verify_otp.html", {"error": "Mobile number and OTP are required."})

        try:
            entered_otp = int(entered_otp)
        except ValueError:
            return render(request, "frontend/verify_otp.html", {"error": "OTP must be a number."})

        if otp_storage.get(mobile) == entered_otp:
            otp_storage.pop(mobile)
            return redirect(reverse("register"))  
        else:
            return render(request, "frontend/verify_otp.html", {"error": "Invalid OTP. Please try again."})

    

class RegisterTemplateView(View):
    def get(self, request):
        return render(request, "frontend/register.html")

    def post(self, request):
        mobile = request.session.get("mobile")
        name = request.POST.get("name")
        password = request.POST.get("password")

        if not mobile or not name or not password:
            return render(request, "frontend/register.html", {
                "error": "Mobile number, name, and password are required.",
                "mobile": mobile,
                "name": name,
            })
            
        User = get_user_model()
        if User.objects.filter(mobile=mobile).exists():
            return render(request, "frontend/register.html", {
                "error": "This mobile number is already registered.",
                "mobile": mobile,
                "name": name,
            })

        User.objects.create_user(mobile=mobile, name=name, password=password)
        return redirect(reverse("login"))




class LoginView(View):
    def get(self, request):
        return render(request, "frontend/login.html")  # نمایش فرم لاگین

    def post(self, request):
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        if not mobile or not password:
            return render(request, "frontend/login.html", {
                "error": "Mobile number and password are required."
            })

        user = authenticate(request, username=mobile, password=password)

        if not user:
            return render(request, "frontend/login.html", {
                "error": "Incorrect mobile number or password."
            })

        login(request, user)
        return redirect("home")

    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


@login_required
def user_profile(request):
    user = request.user
    subscription = user.subscription
    remaining_days = user.remaining_subscription_days()
    context = {
        'user': user,
        'subscription': subscription,
        'remaining_days': remaining_days,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile/update.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile') 
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'profile/change_password.html', {'form': form})

class PurchaseSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subscription_id = request.data.get("subscription_id")
        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user.purchase_subscription(subscription)
        
        return Response({
            "message": "Subscription purchased successfully",
            "subscription": subscription.name,
            "expiry_date": user.subscription_expiry
        }, status=status.HTTP_200_OK)

