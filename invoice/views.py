from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import InvoiceForm, UpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Invoice, Return1, Return2
from accounts.models import User, TaxpayerProfile, OfficialProfile
from notification.models import Notification
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from decimal import *
from datetime import *
from django.core.exceptions import ValidationError
import random
@login_required
def upload(request):
	if request.method == 'POST':
		invoice_form = InvoiceForm(request.POST, request.FILES)
		if invoice_form.is_valid() is not None:
			invoice=Invoice()
			try:
				ob = User.objects.get(gstin=request.POST.get('gstin'))
				if ob.is_taxpayer is True and ob.gstin==request.POST.get('gstin'):
					tax = TaxpayerProfile.objects.get(user=ob)
					invoice.taxpayer = tax
					invoice.file = request.FILES['file']
					off = OfficialProfile.objects.get(aadhar=111111111111)
					invoice.official=random.choice(OfficialProfile.objects.all())
					invoice.save()
					invoice.invoiceNo = invoice.id
					invoice.save()
					return render(request,'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})
				else:
					return HttpResponse('<h1>Go back and submit correct GSTIN</h1>')
			except (User.DoesNotExist):
				return HttpResponse('<h1>Go back and submit correct GSTIN</h1>')

		else:
			invoice_form = InvoiceForm()
			return render(request, 'invoice/invoice_upload.html', {'invoice_form':invoice_form, 'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})

	else:
		invoice_form = InvoiceForm()
		return render(request, 'invoice/invoice_upload.html', {'invoice_form':invoice_form, 'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})

@login_required
def download(request):
	try:
		official = OfficialProfile.objects.get(user=request.user)
		return render(request, 'invoice/invoice_download.html', {'invoices':Invoice.objects.filter(official=official)})
	except OfficialProfile.DoesNotExist:
		return HttpResponse('<h1>Invalid request</h1>')

@login_required
def update(request):
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
		print("22222")
		updateform = UpdateForm(request.POST)
		if updateform.is_valid() is not None:
			try:
				ob = User.objects.get(gstin=request.POST.get('gstin'))
				recipent = User.objects.get(gstin=request.POST.get('recipent_gstin'))
				if ob.is_taxpayer is True and recipent.is_taxpayer is True:
					tax = TaxpayerProfile.objects.get(user=ob)
					receiver = TaxpayerProfile.objects.get(user=recipent)
					invoice = None
					if not str(request.POST.get('invoiceNo')).isdigit():
						return HttpResponse('<h1>Invalid Invoice No.</h1>')
					try:
						invoice = Invoice.objects.get(invoiceNo=request.POST.get('invoiceNo'))
					except Invoice.DoesNotExist:
						return HttpResponse('<h1>Incorrect Invoice No.</h1>')
					status = request.POST.get('status')
					if invoice.taxpayer==tax:
						if status=='verified':
							cgst = request.POST.get('cgst')
							sgst = request.POST.get('sgst')
							igst = request.POST.get('igst')
							gst_rate = request.POST.get('gst_rate')
							value = request.POST.get('value')
							try:
								if float(cgst)<0.0 or float(sgst)<0.0 or float(igst)<0.0 or float(value)<0.0:
									return HttpResponse('<h1>Invalid monetary amount entered</h1>')
							except ValidationError:
								return HttpResponse('<h1>Invalid monetary amount entered</h1>')
							for r in Return1.objects.filter(gstin=ob.gstin):
								if r.to_date.strftime("%Y-%m-%d")<=due and prev<=r.to_date.strftime("%Y-%m-%d") and invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
									invoice.return1 = r
									break
							if cgst==sgst and float(cgst) is not 0.0:
								if Decimal(float(cgst)+float(sgst)).compare(Decimal((Decimal(gst_rate)*Decimal(value))/100))==0:
									tax.output_tax+=Decimal(float(cgst)+float(sgst))
									receiver.input_tax+=Decimal(float(cgst)+float(sgst))
									tax.save()
									receiver.save()
									flag=1
									return22 = Return2.objects.filter(gstin=request.POST.get('recipent_gstin'))
									for r in return22:
										if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d") and invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
											r.input_tax+=Decimal(float(cgst)+float(sgst))
											r.save()
											flag=0
											break
									if flag==1:
										return2 = Return2()
										return2.gstin=request.POST.get('recipent_gstin')
										return2.name=str(recipent.first_name)+' '+str(recipent.last_name)
										return2.due_date=due_date
										return2.input_tax=Decimal(float(cgst)+float(sgst))
										return2.save()

									invoice.verified = True
									invoice.recipent = request.POST.get('recipent_gstin')
									invoice.value = request.POST.get('value')
									invoice.gst_rate = request.POST.get('gst_rate')
									invoice.cgst = request.POST.get('cgst')
									invoice.sgst = request.POST.get('sgst')
									invoice.igst = request.POST.get('igst')
									invoice.due_date = request.POST.get('due_date')
									invoice.save()

								else:
									return HttpResponse('<h1>Wrong tax values</h1>')
							else:
								if Decimal(float(igst)).compare(Decimal((Decimal(gst_rate)*Decimal(value))/100))==0:
									tax.output_tax+=Decimal(float(igst))
									receiver.input_tax+=Decimal(float(igst))
									tax.save()
									receiver.save()
									return22 = Return2.objects.filter(gstin=request.POST.get('recipent_gstin'))
									flsg=1
									for r in return22:
										if r.due_date.strftime("%Y-%m-%d")<=due and prev<=r.due_date.strftime("%Y-%m-%d") and invoice.due_date.strftime("%Y-%m-%d")<=due and prev<=invoice.due_date.strftime("%Y-%m-%d"):
											r.input_tax+=Decimal(float(cgst)+float(sgst))
											r.save()
											flag=0
											break
									if flag==1:
										return2 = Return2()
										return2.gstin=request.POST.get('recipent_gstin')
										return2.name=str(recipent.first_name)+' '+str(recipent.last_name)
										return2.due_date=due_date
										return2.input_tax=Decimal(float(cgst)+float(sgst))
										return2.save()

									invoice.verified = True
									invoice.recipent = request.POST.get('recipent_gstin')
									invoice.value = request.POST.get('value')
									invoice.gst_rate = request.POST.get('gst_rate')
									invoice.cgst = request.POST.get('cgst')
									invoice.sgst = request.POST.get('sgst')
									invoice.igst = request.POST.get('igst')
									invoice.due_date = request.POST.get('due_date')
									invoice.save()

								else:
									return HttpResponse('<h1>Wrong tax values</h1>')
						invoice.checked = True
						invoice.save()
						title=''
						message=''
						title2=''
						message2=''
						if status=='verified':
							title = 'Invoice verified'
							message = 'Invoice No. '+str(invoice.invoiceNo)+' has been verified.'
							title2 = 'An invoice concerning you as recipeent has been verified'
							message2 = 'Invoice No. '+str(invoice.invoiceNo)+' submitted by '+str(ob.first_name)+' '+str(ob.last_name)+' has been verified. Your input tax has been updated. Kindly check in home.'
							n2=Notification()
							n2.title=title2
							n2.message=message2
							n2.user=recipent
							n2.save()
						else:
							title = 'Invoice refuted'
							message = 'Invoice No. '+str(invoice.InvoiceNo)+' has been refuted. No changes have been made to your tax liabilities.'
						n=Notification()
						n.title=title
						n.message=message
						n.user=ob
						n.save()
						print(Notification.objects.filter(user=ob).filter(viewed=False).count())

					else:
						return HttpResponse('<h1>Enter correct GSTIN</h1>')
					return render(request, 'invoice/invoice_download.html', {'invoices':Invoice.objects.all()})

				else:
					return HttpResponse('<h1>Go back and submit correct GSTIN</h1>')
			except (User.DoesNotExist,Invoice.DoesNotExist):
				return HttpResponse('<h1>Go back and submit correct GSTIN and Invoice No</h1>')
			except ValidationError:
				return HttpResponse('<h1>Invalid Date format</h1>')

		else:
			update_form = UpdateForm()
			return render(request, 'invoice/invoice_update.html', {'update_form':update_form})

	else:
		update_form = UpdateForm()
		return render(request, 'invoice/invoice_update.html', {'update_form':update_form})