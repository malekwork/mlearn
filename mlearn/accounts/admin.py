from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subscription
    
class UserAdmin(BaseUserAdmin):
    list_display = ('mobile', 'name', 'is_staff', 'is_superuser','subscription', 'subscription_expiry')
    search_fields = ('mobile', 'name')
    ordering = ('mobile',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password','subscription', 'subscription_expiry')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'name', 'password'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Subscription)

