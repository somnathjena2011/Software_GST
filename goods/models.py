from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as ____
# Create your models here.
class Good(models.Model):
	hsn = models.CharField(max_length=12, unique=False)
	gst = models.DecimalField(max_digits=4, decimal_places=0)
	name = models.CharField(max_length=2000, unique=False)