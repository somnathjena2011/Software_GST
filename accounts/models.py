from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
   # """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
	is_taxpayer = models.BooleanField(default=False)
	is_official = models.BooleanField(default=False)
	first_name = models.CharField(max_length=200,)
	last_name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200, unique=True)
	gstin = models.CharField(max_length=200, unique=True, null=True)
	password = models.CharField(max_length=200)
	username = None
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()


class TaxpayerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='taxpayer_profile')
	aadhar = models.DecimalField(max_digits=12, decimal_places=0, unique=True, null=True)
	input_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
	output_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


class OfficialProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,  related_name='official_profile')
	aadhar = models.DecimalField(max_digits=12, decimal_places=0, null=True,unique=True)
	uid = models.CharField(max_length=200)
