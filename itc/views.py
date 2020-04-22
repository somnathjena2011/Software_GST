from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import ITCForm
from django.contrib.auth.forms import AuthenticationForm
from invoice.models import Invoice, Return1, Return2
from accounts.models import User, TaxpayerProfile, OfficialProfile
from notification.models import Notification
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from decimal import *
from datetime import *

@login_required
def home(request):
	due_date = ''
	due=''
	prev_due=''
	prev=''
	today = date.today()
	today = today.strftime("%Y-%m-%d")
	if today[8]=='0' or today[8:10]=='10':
		due_date = datetime(int(today[:4]),int(today[5:7]),10)
		due = today[:8]+'10'
		if int(today[5:7])==1:
			prev_due = datetime(int(today[:4])-1,12,10)
			prev = str(int(today[:4]-1))+'-'+'12-10'
		else:
			prev_due = datetime(int(today[:4]),int(today[5:7])-1,10)
			prev = prev_due.strftime("%Y-%m-%d")
	elif int(today[5:7])<=11:
		due_date = datetime(int(today[:4]),int(today[5:7])+1,10)
		x = str(int(today[5:7])+1)
		if len(x) == 1:
			x='0'+x
		due = today[:5]+x+'-10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	else:
		due_date = datetime(int(today[:4])+1,1,10)
		x = str(int(today[5:7])+1)
		if len(x) == 1:
			x='0'+x
		due = today[:5]+x+'-10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	return2 =None
	for r in Return2.objects.filter(gstin=request.user.gstin):
		if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d"):
			return2 = r
			break
	return render(request, 'itc/home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False), 'due':due,'prev':prev,'return2':return2})

@login_required
def claim(request):
	due_date = ''
	due=''
	prev_due=''
	prev=''
	today = date.today()
	today = today.strftime("%Y-%m-%d")
	if today[8]=='0' or today[8:10]=='10':
		due_date = datetime(int(today[:4]),int(today[5:7]),10)
		due = today[:8]+'10'
		if int(today[5:7])==1:
			prev_due = datetime(int(today[:4])-1,12,10)
			prev = str(int(today[:4]-1))+'-'+'12-10'
		else:
			prev_due = datetime(int(today[:4]),int(today[5:7])-1,10)
			prev = prev_due.strftime("%Y-%m-%d")
	elif int(today[5:7])<=11:
		due_date = datetime(int(today[:4]),int(today[5:7])+1,10)
		x = str(int(today[5:7])+1)
		if len(x) == 1:
			x='0'+x
		due = today[:5]+x+'-10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	else:
		due_date = datetime(int(today[:4])+1,1,10)
		x = str(int(today[5:7])+1)
		if len(x) == 1:
			x='0'+x
		due = today[:5]+x+'-10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	if request.method == 'POST':
		gstin = request.POST.get('gstin')
		account = request.POST.get('account')
		amount = request.POST.get('amount')
		ifsc = request.POST.get('ifsc')
		ob = request.user
		return2=None
		try:
			if float(amount)<0.0:
				return HttpResponse('<h1>Invalid amount</h1>')
		except ValidationError:
			return HttpResponse('<h1>Invalid amount</h1>')
		if ob.gstin == gstin and ob.is_taxpayer is True:
			tax = TaxpayerProfile.objects.get(user=ob)
			return22 = Return2.objects.filter(gstin=gstin)
			flag=1
			for r in return22:
				if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d"):
					if float(amount)<=float(r.input_tax):
						r.input_tax-=Decimal(amount)
						r.save()
						tax.input_tax-=Decimal(amount)
						tax.save()
					else:
						return HttpResponse('<h1>Amount entered exceeded claimable ITC</h1>')
					return2=r
					flag=0
					break
			if flag==1:
				return HttpResponse('<h1>You cannot claim your ITC yet</h1>')
			return render(request, 'itc/home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False), 'due':due,'prev':prev,'return2':return2})
		else:
			return HttpResponse('<h1>Incorrect GSTIN</h1>')

	else:
		itc_form = ITCForm()
		return render(request,'itc/form.html',{'itc_form':itc_form,'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})
