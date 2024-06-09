from typing import Iterable
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager, Group
from django.core.exceptions import ValidationError


class CustomGroup(Group):
    description = models.TextField(verbose_name="Description", blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name
    

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
    username = models.CharField(max_length=80, unique=True, verbose_name="Nom d'utilisateur")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True, verbose_name="Adresse mail")
    first_name = models.CharField(max_length=80, null=True, verbose_name="Prénom")
    last_name = models.CharField(max_length=80, null=True, verbose_name="Nom")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="Ajouté le")
    groups = models.ManyToManyField(CustomGroup, verbose_name="Groupes", blank=True)

    is_staff = models.BooleanField(default=True, verbose_name="Membre d'équipe")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_superuser = models.BooleanField(default=False, verbose_name="Administrateur")
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects: CustomUserManager = CustomUserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        default_permissions = []
        permissions = [
            ("can_add", "Ajouter - Utilisateur"),
            ("can_change", "Modifier - Utilisateur"),
            ("can_delete", "Supprimer - Utilisateur"),
            ("can_view", "Voir - Utilisateur"),
        ]

    def __str__(self):
        return self.username

    @property
    def fullname(self):
        if self.last_name and self.first_name:
            return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

def pin_code_verification(value: str):
    MIN_LENGTH = 4
    MAX_LENGTH = 6

    if len(value) < MIN_LENGTH or len(value) > MAX_LENGTH:
        raise ValidationError("Le code pin doit contenir de (4-6) caractères inclus")
    
    if not value.isdigit():
        raise ValidationError("Le code pin doit contenir que des chiffres")


class UserPreference(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name="Utilisateur")
    pin_code = models.CharField(max_length=6, blank=True, null=True, 
                                validators=[pin_code_verification], 
                                verbose_name="Code pin")
    