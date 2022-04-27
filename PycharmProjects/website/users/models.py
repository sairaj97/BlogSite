from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class Users (AbstractUser):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    email = models.EmailField(
        verbose_name='email address',
        max_length=30,
        unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"  # make the user log in with the email
    REQUIRED_FIELDS = ["username"]

    #objects = CustomUserManager()


    def __str__(self):
        return self.username


class User_details (models.Model):
    Male = 'M'
    FeMale = 'F'
    GENDER_CHOICES = (
        (Male, 'Male'),
        (FeMale, 'Female'),
    )
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              default=Male)
    address = models.TextField(max_length=150, null=False)


class Post (models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    blog_title = models.CharField(max_length=200, null=False)
    post_here = models.TextField(max_length=500, null=False)
    time_stamp = models.DateTimeField(default=timezone.now)


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)
