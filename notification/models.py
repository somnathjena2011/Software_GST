from django.db import models
from accounts.models import User, TaxpayerProfile, OfficialProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Notification(models.Model):
 	title = models.CharField(max_length=256)
 	message = models.TextField()
 	viewed = models.BooleanField(default=False)
 	user = models.ForeignKey(User, on_delete=models.CASCADE)

