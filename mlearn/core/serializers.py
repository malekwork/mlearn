from rest_framework import serializers
from accounts.models import Subscription
from .models import Category, Post, Comment
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
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'video', 'is_premium', 'category', 'author', 'created_at', 'comments']
        extra_kwargs = {
            'author': {'read_only': True}, 
            'created_at': {'read_only': True}     
        }

    def get_comments(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if obj.is_premium:
            if not user or not user.is_authenticated:
                return []
            if not (user.subscription and user.remaining_subscription_days() > 0 and user != obj.author):
                return []

        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            user = request.user
            has_valid_subscription = user.subscription and user.remaining_subscription_days() > 0 and user != instance.author

            if instance.is_premium and not has_valid_subscription:
                return {
                    "id": data["id"],
                    "title": data["title"],
                    "image": data["image"]
                }

        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        extra_kwargs = {
            'author': {'read_only': True},
            'created_at': {'read_only': True},
        }