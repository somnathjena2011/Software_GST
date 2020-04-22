from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth.models import User
from .models import User, TaxpayerProfile, OfficialProfile

class TaxpayerBackend(ModelBackend):
	def authenticate(self, request, **kwargs):
		email = kwargs['email']
		password = kwargs['password']
		try:
			user = User.objects.get(email=email)
			if user.check_password(password)==True and user.is_taxpayer==True:
				return user
			else:
				pass
		except User.DoesNotExist:
			pass

class OfficialBackend(ModelBackend):
	def authenticate(self, request, **kwargs):
		email = kwargs['email']
		password = kwargs['password']
		try:
			official = User.objects.get(email=email)
			if user.check_password(password)==True and user.is_official==True:
				return user
			else:
				pass
		except User.DoesNotExist:
			pass
