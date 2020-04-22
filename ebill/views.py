from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from .forms import BillForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Bill
from accounts.models import User, TaxpayerProfile, OfficialProfile
from datetime import date, datetime, timedelta
from django.template.loader import get_template
from .utils import render_to_pdf
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from goods.models import Good
from decimal import *
from django.core.exceptions import ValidationError
@login_required
def generate_view(request, bill):
	return render(request, 'ebill/pdf.html', {'bill':bill})

@login_required
def ebill_view(request):
	if request.method == 'POST':
		bill_form = BillForm(request.POST)
		if bill_form.is_valid() is not None:
			bill=Bill()
			bill.tr_type=request.POST.get('tr_type')
			bill.sub_type=request.POST.get('sub_type')
			bill.validFrom=request.POST.get('validFrom')
			bill.distance=bill_form.data['distance']
			bill.validTo=request.POST.get('validTo')
			bill.from_name=bill_form.data['from_name']
			bill.from_address=bill_form.data['from_address']
			bill.from_pin=bill_form.data['from_pin']
			bill.to_name=bill_form.data['to_name']
			bill.to_address=bill_form.data['to_address']
			bill.to_pin=bill_form.data['to_pin']
			bill.generator_gstin=bill_form.data['generator_gstin']
			bill.recipent_gstin=bill_form.data['recipent_gstin']
			bill.product_name=bill_form.data['product_name']
			bill.hsn=bill_form.data['hsn']
			bill.value=bill_form.data['value']
			bill.tax_rate=request.POST.get('tax_rate')
			bill.tax_amt=bill_form.data['tax_amt']
			bill.cgst=bill_form.data['cgst']
			bill.sgst=bill_form.data['sgst']
			bill.igst=bill_form.data['igst']
			bill.transportNo=bill_form.data['transportNo']
			bill.distance=bill_form.data['distance']
			if bill.generator_gstin==bill.recipent_gstin:
				return HttpResponse('<h1>Both Generator and Recipent GSTIN are same</h1>')
			try:
				ft=float(bill.value)+float(bill.tax_amt)+float(bill.cgst)+float(bill.sgst)+float(bill.igst)
			except ValueError:
				return HttpResponse('<h1>Incorrect monetary amount entered in form</h1>')
			if float(bill.value)<0.0 or float(bill.tax_amt)<0.0 or float(bill.cgst)<0.0 or float(bill.sgst)<0.0 or float(bill.igst)<0.0:
				return HttpResponse('<h1>Incorrect monetary amount entered in form</h1>')
			if not str(bill.from_pin).isdigit() or not str(bill.to_pin).isdigit():
				return HttpResponse('<h1>Incorrect PIN</h1>')
			if len(str(bill.generator_gstin))!=14 or len(str(bill.recipent_gstin))!=14:
				return HttpResponse('<h1>GSTIN must be of 14 characters</h1>')
			elif float(bill.value)<50000.00:
				return HttpResponse('<h1>Value of goods must be at least 50000.00</h1?')
			else: 
				try:
					ob1=User.objects.get(gstin=bill.recipent_gstin)
					ob2=User.objects.get(gstin=bill.generator_gstin)
					if ob1.is_taxpayer and ob2.is_taxpayer and (ob2==request.user or ob1==request.user) :
						try:
							gd = Good.objects.filter(hsn=bill.hsn)
							gud=''
							if gd is not None:
								flag=0
								for gg in gd:
									if int(gg.gst)==int(bill.tax_rate):
										flag=1
										gud=gg
										break
								if flag==0:
									return HttpResponse('<h1>Incorrect HSN or GST rate entered</h1>')
							else:
								return HttpResponse('<h1>Incorrect HSN entered</h1>')
							if int(gud.gst)==int(bill.tax_rate):
								if float(bill.tax_amt)==float((float(gud.gst)*float(bill.value))/100) and bill.igst==bill.tax_amt and bill.cgst==bill.sgst and float(bill.cgst)==float(bill.igst)/2:
									try:
										bill.save()
										bill.billno=bill.id
										bill.save()
									except ValidationError:
										return HttpResponse('<h1>Invalid date format</h1>')
								else:
									return HttpResponse('<h1>Incorrect tax amount</h1>')
							else:
								return HttpResponse('<h1>Incorrect tax slab chosen</h1>')
						except (Good.DoesNotExist):
							return HttpResponse('<h1>Incorrect HSN entered</h1>')
						except ValueError:
							return HttpResponse('<h1>Invalid monetary amount entered</h1>')
					else:
						return HttpResponse('<h1>Incorrect GSTIN</h1>')
					render(request, 'ebill/pdf.html', {'bill':bill})
					pdf = render_to_pdf('ebill/pdf.html',{'bill':bill})
					return HttpResponse(pdf, content_type='application/pdf')
				except (User.DoesNotExist):
					return HttpResponse('<h1>Invalid data</h1>')

		else:
			bill_form = BillForm()
			return render(request, 'ebill/ebill.html', {'bill_form':bill_form})

	else:
		bill_form = BillForm()
		return render(request, 'ebill/ebill.html', {'bill_form':bill_form})


