from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def __str__(self):
        return self.mobile
