from rest_framework import serializers
from accounts.models import Subscription
from .models import Category, Post
from mptt.templatetags.mptt_tags import cache_tree_children

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)



class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        children = obj.get_children()
        return CategorySerializer(children, many=True).data



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'video', 'is_premium', 'category', 'author', 'created_at']

        extra_kwargs = {
            'author': {'read_only': True}, 
            'created_at': {'read_only': True}
        }