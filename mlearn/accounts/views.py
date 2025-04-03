import random
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions
from django.contrib.auth import update_session_auth_hash
from .models import User, Subscription
from .serializers import (
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)

otp_storage = {}  # Temporary storage for OTPs

class SendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        if mobile is None:
            return Response({"error": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        otp_storage[mobile] = otp  # Store OTP
        print(f"OTP for {mobile}: {otp}")  # Simulate sending SMS
        return Response({"message": "OTP has been sent."}, status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        otp = request.data.get("otp")

        if mobile is None or otp is None:
            return Response({"error": "Mobile number and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = int(otp)
        if otp_storage.get(mobile) == otp:
            otp_storage.pop(mobile)  # Remove OTP after verification
            return Response({"message": "OTP verified. Proceed with registration."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        name = request.data.get("name")
        password = request.data.get("password")
        
        if mobile is None or name is None or password is None:
            return Response({"error": "Mobile number, name, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(mobile=mobile).exists():
            return Response({"error": "This mobile number is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(mobile=mobile, name=name, password=password)
        return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")
        
        if mobile is None or password is None:
            return Response({"error": "Mobile number and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, mobile=mobile)

        if not check_password(password, user.password):
            return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


class CheckLoginStatusView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"logged_in": True, "mobile": user.mobile, "name": user.name}, status=status.HTTP_200_OK)
    

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"error": "Old password is incorrect"}, status=400)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            update_session_auth_hash(request, user)
            return Response({"message": "Password changed successfully"})

        return Response(serializer.errors, status=400)
    


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

