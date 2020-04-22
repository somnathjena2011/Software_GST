from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import OfficialProfileForm, TaxpayerProfileForm, UserForm, TaxpayerLoginForm, OfficialLoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, TaxpayerProfile, OfficialProfile
from .backends import TaxpayerBackend, OfficialBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from invoice.models import Invoice
from notification.models import Notification
from decimal import *
from django.core.exceptions import ValidationError

def choose(request):
	return render(request, 'accounts/choose.html')	

def taxpayer_home(request):
	try:
		return render(request, 'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})
	except (TypeError):
		return render(request, 'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all()})

def official_home(request):
	return render(request, 'accounts/official_home.html', {'off':OfficialProfile.objects.all()})	

def taxpayer_profile_view(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		taxpayer_profile_form = TaxpayerProfileForm(request.POST)
		if user_form.is_valid() is not None:
			user=User()
			user.first_name=user_form.data['first_name']
			user.last_name=user_form.data['last_name']
			user.email=user_form.data['email']
			user.password=user_form.data['password']
			user.is_taxpayer=True
			tax=TaxpayerProfile()
			tax.user=user
			tax.aadhar=taxpayer_profile_form.data['aadhar']
			if not str(tax.aadhar).isdigit():
				return HttpResponse('<h1>Please enter a valid AADHAR</h1>')
			user.gstin=tax.aadhar+user.first_name[0:2]
			if len(str(tax.aadhar))!=12:
				return HttpResponse('<h1>AADHAR must be 12 digit</h1>')
			else: 
				try:
					ob1=TaxpayerProfile.objects.get(aadhar=tax.aadhar) 
					ob2=User.objects.get(gstin=user.gstin)
					ob3=User.objects.get(email=user.email)
					return HttpResponse('<h1>User exists</h1>') 
				except (User.DoesNotExist,TaxpayerProfile.DoesNotExist):
					user.save()
					tax.user=user
					tax.save()
					login(request, user, backend='accounts.backends.TaxpayerBackend')
					return render(request, 'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=user).filter(viewed=False)})

		else:
			user_form = UserForm()
			taxpayer_profile_form = TaxpayerProfileForm()
			return render(request, 'accounts/taxpayer_profile.html', {'user_form':user_form, 'taxpayer_profile_form':taxpayer_profile_form})

	else:
		user_form = UserForm()
		taxpayer_profile_form = TaxpayerProfileForm()
		return render(request, 'accounts/taxpayer_profile.html', {'user_form':user_form, 'taxpayer_profile_form':taxpayer_profile_form})


def official_profile_view(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		official_profile_form = OfficialProfileForm(request.POST)
		if user_form.is_valid() is not None :
			user=User()
			user.first_name=user_form.data['first_name']
			user.last_name=user_form.data['last_name']
			user.email=user_form.data['email']
			user.password=user_form.data['password']
			user.is_official=True
			official=OfficialProfile()
			official.user=user
			official.aadhar=official_profile_form.data['aadhar']
			if not str(official.aadhar).isdigit():
				return HttpResponse('<h1>Please enter a valid AADHAR</h1>')
			official.uid=official_profile_form.data['uid']
			user.gstin=official.aadhar+user.first_name[0:2]
			if len(str(official.aadhar))!=12:
				return HttpResponse('<h1>AADHAR must be 12 digit</h1>')
			else: 
				try:
					ob1=OfficialProfile.objects.get(aadhar=official.aadhar) 
					ob2=User.objects.get(gstin=user.gstin)
					ob3=User.objects.get(email=user.email)
					ob4=OfficialProfile.objects.get(uid=official.uid)
					return HttpResponse('<h1>User exists</h1>') 
				except (User.DoesNotExist,OfficialProfile.DoesNotExist):
					user.save()
					official.user=user
					official.save()
					login(request, user, backend='accounts.backends.OfficialBackend')
					return render(request, 'accounts/official_home.html', {'off':OfficialProfile.objects.all()})

		else:
			user_form = UserForm()
			official_profile_form = OfficialProfileForm()
			return render(request, 'accounts/official_profile.html', {'user_form':user_form, 'official_profile_form':official_profile_form})

	else:
		user_form = UserForm()
		official_profile_form = OfficialProfileForm()
		return render(request, 'accounts/official_profile.html', {'user_form':user_form, 'official_profile_form':official_profile_form})

def taxpayer_login(request):
	if request.method == 'POST':
		form = TaxpayerLoginForm(request.POST)
		if form.is_valid() is not None:
			user=User()
			email=form.data['email']
			password=form.data['password']
			try:
				ob1=User.objects.get(email=email)
				if ob1.password == password:
					if ob1.is_taxpayer is True:
						login(request, ob1, backend='accounts.backends.TaxpayerBackend')
						return render(request, 'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=ob1).filter(viewed=False)})
					else:
						return HttpResponse("<h1>No such user</h1>")
				else:
					return HttpResponse("<h1>Incorrect Password")
			except (User.DoesNotExist, TaxpayerProfile.DoesNotExist):
				return HttpResponse("<h1>No such user</h1>")
	else:
		form=TaxpayerLoginForm()
	return render(request,"accounts/taxpayer_login.html",{'form':form})

def official_login(request):
	if request.method == 'POST':
		form = OfficialLoginForm(request.POST)
		if form.is_valid() is not None:
			user=User()
			email=form.data['email']
			password=form.data['password']
			try:
				ob1=User.objects.get(email=email)
				if ob1.password == password:
					if ob1.is_official is True:
						login(request, ob1, backend='accounts.backends.OfficialBackend')
						return render(request, 'accounts/official_home.html', {'off':OfficialProfile.objects.all()})
					else:
						return HttpResponse("<h1>No such user</h1>")
				else:
					return HttpResponse("<h1>Incorrect Password</h1>")
			except (OfficialProfile.DoesNotExist):
				return HttpResponse("<h1>No such user</h1>")
	else:
		form=OfficialLoginForm()
		return render(request,"accounts/official_login.html",{'form':form})

def taxpayer_logout(request):
	logout(request)
	#messages.info(request, "Logged out successfully!")
	return render(request, 'accounts/choose.html')

def official_logout(request):
	logout(request)
	#messages.info(request, "Logged out successfully!")
	return render(request, 'accounts/choose.html')
