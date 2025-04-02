from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, name=None):
        if not mobile:
            raise ValueError("Mobile number is required")
        user = self.model(mobile=mobile, name=name)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        user = self.create_user(mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_expiry = models.DateField(null=True, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    
    def remaining_subscription_days(self):
        if self.subscription and self.subscription_expiry:
            days_left = (self.subscription_expiry - now().date()).days
            return max(days_left, 0) # Return 0 if subscription has expired
        return 0

    def purchase_subscription(self, subscription):
        self.subscription = subscription
        self.subscription_expiry = now().date() + timedelta(days=subscription.duration_days)
        self.save()

    def __str__(self):
        return self.mobile
