from django.shortcuts import render
from django.urls import reverse
#from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from accounts.models import User,TaxpayerProfile,OfficialProfile
from invoice.models import Invoice, Return1, Return2
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import CardForm, NetForm
from datetime import date, datetime
from decimal import *
# Create your views here.

#@csrf_exempt
#def payment_done(request):
#	return render(request,'accounts/taxpayer_home.html')

#@csrf_exempt
#def payment_canceled(request):
#	return render(request,'accounts/taxpayer_home.html')

#@login_required
#def payment_process(request):
#	user = request.user
#	tax_obj = None
#	for tax in TaxpayerProfile.objects.all():
#		if tax.user == user:
#			tax_obj = tax
#			break

#	paypal_dict = {
#		'business': 'somnathjena.2011@gmail.com',
#		'amount': str(tax_obj.input_tax),
#		'currency_code': 'INR',
#		'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
#		'return_url': request.build_absolute_uri(reverse('payment:done')),
#		'cancel_return': request.build_absolute_uri(reverse('payment:canceled')),
#	}

#	form = PayPalPaymentsForm(initial=paypal_dict)
#	context = {'form': form}
#	return render(request, 'payment/process.html', context)

@login_required
def payment_home(request):
	tax=None
	for t in TaxpayerProfile.objects.all():
		if t.user == request.user:
			tax=t
			break
	return render(request,'payment/home.html',{'invoices':Invoice.objects.all(),'tax':tax,'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})

@login_required
def card(request):
	if request.method=='POST':
		gstin = request.POST.get('gstin')
		if request.user.gstin == gstin:
			expiry = request.POST.get('expiry')
			today = date.today().strftime("%Y-%m-%d")
			if not len(expiry)==5:
				return HttpResponse('<h1>Invalid expiry date</h1>')
			if not str(expiry[:2]).isdigit() or not str(expiry[3:]).isdigit() or expiry[2]!='/':
				return HttpResponse('<h1>Invalid expiry date</h1>')
			if str(expiry[3:]+'/'+expiry[:2])>=str(today[2:4]+'/'+today[5:7]):
				cvv = request.POST.get('cvv')
				if not str(cvv).isdigit():
					return HttpResponse('<h1>Invalid CVV</h1>')
				if len(cvv)==3:
					amount = request.POST.get('amount')
					tax = TaxpayerProfile.objects.get(user=request.user)
					try:
						if float(amount)<0.0:
							return HttpResponse('<h1>Invalid amount</h1>')
					except ValueError:
						return HttpResponse('<h1>Invalid amount</h1>')
					if float(amount)<=float(tax.output_tax):
						print('india')
						tax.output_tax-=Decimal(amount)
						print(tax.output_tax)
						tax.save()
						n=Notification()
						title='Payment successful'
						message='Your tax payment of Rs.'+str(amount)+'was successful. Your current tax liability is Rs. '+str(tax.output_tax)
						n.title=title
						n.message=message
						n.user=request.user
						n.save()
						return render(request,'payment/home.html',{'invoices':Invoice.objects.all(),'tax':tax,'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})
					else:
						return HttpResponse('<h1>Incorrect amount entered</h1>')
				else:
					return HttpResponse('<h1>Invalid CVV</h1>')
			else:
				return HttpResponse('<h1>Your card has expired</h1>')
		else:
			return HttpResponse('<h1>Incorrect GSTIN</h1>')
	else:
		cardform=CardForm()
		return render(request,'payment/card.html',{'cardform':cardform})

@login_required
def netbanking(request):
	if request.method=='POST':
		gstin = request.POST.get('gstin')
		if request.user.gstin == gstin:
			amount = request.POST.get('amount')
			try:
				if float(amount)<0.0:
					return HttpResponse('<h1>Invalid amount</h1>')
			except ValueError:
				return HttpResponse('<h1>Invalid amount</h1>')
			try:
				tax =TaxpayerProfile.objects.get(user=request.user)
				if float(amount)<=float(tax.output_tax):
					tax.output_tax-=Decimal(amount)
					tax.save()
					n=Notification()
					title='Payment successful'
					message='Your tax payment of Rs.'+str(amount)+'was successful. Your current tax liability is Rs. '+str(tax.output_tax)
					n.title=title
					n.message=message
					n.user=request.user
					n.save()
					return render(request,'payment/home.html',{'invoices':Invoice.objects.all(),'tax':tax,'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})
				else:
					return HttpResponse('<h1>Incorrect amount entered</h1>')
			except TaxpayerProfile.DoesNotExist:
				return HttpResponse('<h1>Incorrect GSTIN entered</h1>')
		else:
			return HttpResponse('<h1>Incorrect GSTIN</h1>')
	else:
		netform=NetForm()
		return render(request,'payment/net.html',{'netform':netform})