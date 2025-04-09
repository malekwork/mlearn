from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from accounts.models import Subscription
from rest_framework import generics
from .models import Category
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post, Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PostForm, SubscriptionForm
from django.http import HttpResponseForbidden
from .models import Category
from .forms import CategoryForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q

def index_view(request):
    posts = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts, 6)
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
        'page_obj': page_obj,
    }
    return render(request, 'frontend/index.html', context)


def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, "subscriptions/subscription_list.html", {"subscriptions": subscriptions})

def subscription_create(request):
    if not request.user.is_staff:  
        return HttpResponseForbidden("You do not have permission to create a subscrition.")
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subscription_list")
    else:
        form = SubscriptionForm()

    return render(request, "subscriptions/subscription_form.html", {"form": form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "categories/category_list.html", {"categories": categories})

def category_create(request):
    if not request.user.is_staff:  
        return HttpResponseForbidden("You do not have permission to create a category.")
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        parent_categories = Category.objects.filter()
        form = CategoryForm()

    return render(request, "categories/category_form.html", {
        "form": form,
        "parent_categories": parent_categories 
    })

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')

    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'categories/category_posts.html', context)



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if post.is_premium and not request.user.is_authenticated:
        return redirect("login")

    access = True
    if post.is_premium:
        if not ((request.user.subscription and request.user.remaining_subscription_days() > 0) or request.user == post.author):
            access = False

    related_posts = Post.objects.filter(
        Q(category=post.category) | Q(category__in=post.category.get_ancestors())
    ).exclude(id=post.id).order_by('-created_at')[:5]

    context = {
        'post': post,
        'comments': comments,
        'access': access,
        'related_posts': related_posts,
    }

    return render(request, "posts/post_detail.html", context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {"form": form})

def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "posts/comment_form.html", {"form": form, "post": post})
