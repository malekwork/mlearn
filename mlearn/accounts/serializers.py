from rest_framework import serializers
from .models import User, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'duration_days']

class UserProfileSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['mobile', 'name', 'subscription', 'remaining_days']

    def get_remaining_days(self, obj):
        return obj.remaining_subscription_days()

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
