from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('', index_view, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


