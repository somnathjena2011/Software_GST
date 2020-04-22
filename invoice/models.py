from django.db import models
from accounts.models import TaxpayerProfile, OfficialProfile, User
class Return1(models.Model):
	name = models.CharField(max_length=200,)
	gstin = models.CharField(max_length=200, null=True)
	from_date = models.DateField()
	to_date = models.DateField()
	output = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	filed = models.BooleanField(default=False)

class Return2(models.Model):
	name = models.CharField(max_length=200,)
	gstin = models.CharField(max_length=200, null=True)
	due_date = models.DateField(default='2020-05-10')
	input_tax = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	filed = models.BooleanField(default=True)

class Invoice(models.Model):
	invoiceNo = models.IntegerField(null=True)
	taxpayer = models.ForeignKey(TaxpayerProfile, on_delete=models.CASCADE)
	official = models.ForeignKey(OfficialProfile, on_delete=models.CASCADE)
	return1 = models.ForeignKey(Return1, on_delete=models.CASCADE, null=True)
	file = models.FileField(max_length=5000)
	value = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	due_date = models.DateField(default='2020-05-10')
	gst_rate = models.DecimalField(max_digits=4, decimal_places=0, default=0)
	cgst = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	sgst = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	igst = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	recipent = models.CharField(max_length=200, null=True)
	verified = models.BooleanField(default=False)
	checked = models.BooleanField(default=False)