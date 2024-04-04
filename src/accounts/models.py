from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self._create_user(username, email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def fullname(self):
        if self.last_name and self.first_name:
            return f"{self.first_name} {self.last_name}"


