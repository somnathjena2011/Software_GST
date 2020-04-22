from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from invoice.models import Invoice, Return1, Return2
from accounts.models import User, TaxpayerProfile, OfficialProfile
from notification.models import Notification
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from decimal import *
from datetime import date, datetime, timedelta
from .utils import render_to_pdf
from dateutil.relativedelta import relativedelta
from .forms import ReturnForm
from django.core.exceptions import ValidationError
@login_required
def gstr1_view(request):
	usr = request.user
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
		due = str(int(today[:5])+1)+str(int(today[5:7])+1)+'10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	invoices=[]
	return1=None
	tax=TaxpayerProfile.objects.get(user=usr)
	invoices2=Invoice.objects.filter(taxpayer=tax).filter(verified=True)	
	return12 = None
	try:	
		return12 = Return1.objects.filter(gstin=usr.gstin)
		for r in return12:
			if r.to_date.strftime("%Y-%m-%d")<=due and prev<=r.to_date.strftime("%Y-%m-%d"):
				return1=r
				break
		for invoice in invoices2:
			if invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
				invoices.append(invoice)
				invoice.return1 = return1
				invoice.save()
	except(Return1.DoesNotExist):
		return12=None
		return HttpResponse('<h1>Your Return could not be filed</h1>')
	if return1 is not None:
		render(request, 'gstreturn/pdf.html', {'return1':return1,'user':request.user,'invoices':invoices,'notifs':Notification.objects.filter(user=usr).filter(viewed=False)})
		pdf = render_to_pdf('gstreturn/pdf.html',{'return1':return1,'user':request.user,'invoices':invoices})
		return HttpResponse(pdf, content_type='application/pdf')
	else:
		return HttpResponse('<h1>Your Return could not be filed</h1>')

@login_required
def gstr2_view(request):
	usr = request.user
	due_date = ''
	due=''
	today = date.today()
	today = today.strftime("%Y-%m-%d")
	prev_due=''
	prev=''
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
		due = str(int(today[:5])+1)+str(int(today[5:7])+1)+'10'
		prev_due = datetime(int(today[:4]),int(today[5:7]),10)
		prev=prev_due.strftime("%Y-%m-%d")
	return2=None
	invoices=[]
	return22 = None
	invoices2=Invoice.objects.filter(recipent=usr.gstin).filter(verified=True)
	try:	
		return22 = Return2.objects.filter(gstin=usr.gstin)
		for r in return22:
			if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d"):
				return2=r
				break		
	except(Return2.DoesNotExist):
		return22=None
	if invoices2 is not None:
		for invoice in invoices2:
			if invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
				invoices.append(invoice)
	if return2 is not None:
		render(request, 'gstreturn/pdf2.html', {'return2':return2,'user':request.user,'invoices':invoices})
		pdf = render_to_pdf('gstreturn/pdf2.html',{'return2':return2,'user':request.user,'invoices':invoices})
		return HttpResponse(pdf, content_type='application/pdf')
	else:
		return HttpResponse('<h1>Your Return2 could not be filed</h1>')

@login_required
def upload(request):
	usr = request.user
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
	tax= TaxpayerProfile.objects.get(user=usr)
	return2=None
	return1=None
	invoices=[]	
	return22 = None
	invoices2=Invoice.objects.filter(recipent=usr.gstin).filter(verified=True)
	try:	
		return22 = Return2.objects.filter(gstin=usr.gstin)
		for r in return22:
			if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d"):
				return2=r
				break		
	except(Return2.DoesNotExist):
		return22=None
	try:	
		return12 = Return1.objects.filter(gstin=usr.gstin)
		for r in return12:
			if r.to_date.strftime("%Y-%m-%d")<=due and prev<=r.to_date.strftime("%Y-%m-%d"):
				return1=r
				break		
	except(Return1.DoesNotExist):
		return12=None
	return render(request,'gstreturn/gstr.html',{'return1':return1,'return2':return2, 'due':due,'notifs':Notification.objects.filter(user=usr).filter(viewed=False)})		

@login_required
def create_view(request):
	if request.method=='POST':
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
		return_form = ReturnForm(request.POST)
		if return_form.is_valid() is not None:
			return1=Return1()
			return1.name=request.POST.get('name')
			return1.gstin=request.POST.get('gstin')
			try:
				return1.from_date=request.POST.get('from_date')
				return1.to_date=request.POST.get('to_date')
			except ValidationError:
				return HttpResponse('<h1>Invalid Date format</h1>')
			tax=None
			try:
				tax = TaxpayerProfile.objects.get(user=request.user)
			except (TaxpayerProfile.DoesNotExist):
				return HttpResponse('<h1>No such taxpayer</h1>')
			if not (request.user.gstin==request.POST.get('gstin')):
				return HttpResponse('<h1>Invalid GSTIN</h1>')
			return12=Return1.objects.filter(gstin=request.POST.get('gstin'))
			for r in return12:
				if r.to_date.strftime("%Y-%m-%d")<=due and prev<=r.to_date.strftime("%Y-%m-%d"):
					return HttpResponse('<h1>You have alredy created a GST Return Form. Move ahead to file it<h1>')
			try:
				return1.save()
			except ValidationError:
				return HttpResponse('<h1>Invalid date format</h1>')
			for invoice in Invoice.objects.filter(taxpayer=tax).filter(verified=True):
				if invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
					invoice.return1 = return1
					invoice.save()
			return HttpResponse('<h1>Thanks</h1>')
		
	else:
		return_form = ReturnForm()
		return render(request,'gstreturn/returnform.html',{'return_form':return_form})