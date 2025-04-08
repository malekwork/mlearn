from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from accounts.models import Subscription
from accounts.serializers import SubscriptionSerializer
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer



class SubscriptionListCreateView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        post = serializer.validated_data['post']

        if post.is_premium:
            if not (user.subscription and user.remaining_subscription_days() > 0 and user != post.author):
                raise serializers.ValidationError("You need a valid subscription to comment on this premium post.")

        serializer.save(author=user)
