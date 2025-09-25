# register, login + otp bn qilishni ko'ramiz
# OTP -> one time password(6 talik kod)
import datetime

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, phone, password, **extra_fields):  # is_staff, s
        user = self.model(
            phone=phone,
            **extra_fields
        )
        user.set_password(str(password))
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        print("\n\nextraa-> fields", extra_fields)
        return self.create_user(phone=phone, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=56)
    phone = models.CharField(max_length=15, unique=True)     # username_field
    user_type = models.SmallIntegerField(default=2, choices=[
        (1, "Admin"),    # dashboardga kira oladigan odam
        (2, "User"),     # oddiy saytdan ro'yxatdan o'tgan odam

    ], verbose_name="Admin(1), User(2)")  # role

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["user_type"]


class Otp(models.Model):
    mobile = models.CharField(max_length=15)
    key = models.CharField(max_length=256)  # 6 talik kod -> shifrlash

    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    by = models.CharField(choices=[
        ("login", "Login"),
        ("regis", "Register"),
    ])
    extra = models.JSONField(default=dict)
    tries = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def check_date(self):
        now = datetime.datetime.now()
        if (now-self.created).total_seconds() > 3*60:
            return False
        return True

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        if self.is_confirmed:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)











