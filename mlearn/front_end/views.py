from django.shortcuts import render

def index_view(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user
    }
    return render(request, 'frontend/index.html', context)

def send_otp(request):
    return render(request, 'frontend/send_otp.html')

def verify_otp(request):
    return render(request, 'frontend/verify_otp.html')

def register(request):
    return render(request, 'frontend/register.html')


def login(request):
    return render(request, 'frontend/login.html')



