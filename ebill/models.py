from django.db import models
#from django.contrib.auth.models import AbstractUser, BaseUserManager
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from django.utils.translation import ugettext_lazy as _

class Bill(models.Model):
	tr_type = models.CharField(max_length=10, default='inward')
	sub_type = models.CharField(max_length=10)
	#date=models.DateField()
	billno = models.IntegerField(null=True)
	generator_gstin = models.CharField(max_length=14)
	from_name = models.CharField(max_length=200)
	from_address = models.CharField(max_length=200)
	from_pin = models.IntegerField()
	recipent_gstin = models.CharField(max_length=14)
	to_name = models.CharField(max_length=200)
	to_address = models.CharField(max_length=200)
	to_pin = models.IntegerField()
	product_name = models.CharField(max_length=2000)
	hsn = models.CharField(max_length=10)
	value = models.DecimalField(max_digits=50,decimal_places=2)
	tax_rate = models.DecimalField(max_digits=4, decimal_places=0)
	tax_amt = models.DecimalField(max_digits=50, decimal_places=2)
	cgst = models.DecimalField(max_digits=50, decimal_places=2)
	sgst = models.DecimalField(max_digits=50, decimal_places=2)
	igst = models.DecimalField(max_digits=50, decimal_places=2)
	transportNo = models.CharField(max_length=20)
	distance = models.DecimalField(max_digits=10, decimal_places=3)
	validFrom = models.DateField()
	validTo = models.DateField()
	delivered = models.BooleanField(default=False)

