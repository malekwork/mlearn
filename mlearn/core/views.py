from accounts.models import Subscription
from .models import Post, Category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .forms import CategoryForm, CommentForm, PostForm, SubscriptionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from azbankgateways import bankfactories
from azbankgateways import models as bank_models, default_settings as settings
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model


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


def purchase_subscription_view(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)

    user = request.user 

    factory = bankfactories.BankFactory()
    bank = factory.auto_create()
    bank.set_request(request)
    bank.set_client_callback_url(reverse("callback-gateway"))
    bank.set_mobile_number(user.mobile)
    bank.set_amount(int(subscription.price))
    
    bank_record = bank.ready()
    bank_record.extra_information = {
        "user_id": user.id,
        "subscription_id": subscription.id,
    }
    bank_record.save()

    return bank.redirect_gateway()


def callback_gateway_view(request):
    User = get_user_model()
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404("کد پیگیری نامعتبر است")

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404("رکورد پرداخت پیدا نشد")

    if bank_record.is_success:
        user_id = bank_record.extra_information.get("user_id")
        subscription_id = bank_record.extra_information.get("subscription_id")

        try:
            user = User.objects.get(id=user_id)
            subscription = Subscription.objects.get(id=subscription_id)
        except (User.DoesNotExist, Subscription.DoesNotExist):
            return HttpResponse("اطلاعات کاربر یا اشتراک نامعتبر است.")

        user.purchase_subscription(subscription)
        return HttpResponse("پرداخت موفق! اشتراک شما فعال شد.")

    return HttpResponse("پرداخت ناموفق بود. در صورت کسر مبلغ، بازگشت انجام خواهد شد.")