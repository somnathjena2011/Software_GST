from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Invoice
#from .backends import TaxpayerBackend, OfficialBackend
#import re

class InvoiceForm(forms.Form):
	gstin = forms.CharField(max_length=14, label='GSTIN',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	file = forms.FileField(label='FILE')
	class Meta:
		#model = Invoice
		fields = ['gstin', 'file']
		widgets = {
			'gstin': forms.TextInput(),
			'file': forms.FileInput()
		}
class UpdateForm(forms.Form):
	gstin = forms.CharField(max_length=14, label='GSTIN of Taxpayer',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	invoiceNo = forms.IntegerField(label='Invoice No.',widget=forms.TextInput(attrs={'placeholder':'0'}))
	#inputTax = forms.DecimalField(max_digits=50, decimal_places=2, label='Update Input Tax')
	#outputTax = forms.DecimalField(max_digits=50, decimal_places=2, label='Update Output Tax')
	CHOICES= [
		('verified', 'Verified'),
		('refuted', 'Refuted'),
	]
	TAX = (
		(0,'0'),
		(5,'5'),
		(12,'12'),
		(18,'18'),
		(28,'28'),
	)	
	value = forms.DecimalField(max_digits=50, decimal_places=2, label='VALUE OF GOODS/SERVICE',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	gst_rate = forms.TypedChoiceField(choices=TAX, label='Tax rate', coerce=int)
	cgst = forms.DecimalField(max_digits=50, decimal_places=2, label='CGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	sgst = forms.DecimalField(max_digits=50, decimal_places=2, label='SGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	igst = forms.DecimalField(max_digits=50, decimal_places=2, label='IGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	recipent_gstin = forms.CharField(max_length=14, label='GSTIN of Recipent',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	due_date = forms.DateField(label='Due Date',widget=forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}))
	status = forms.ChoiceField(choices=CHOICES, label='Official status:')
	class Meta:
		fields = ['gstin', 'invoiceNo', 'value', 'gst_rate', 'cgst', 'sgst', 'igst', 'recipent_gstin', 'due_date', 'status']
		widgets = {
			'gstin': forms.TextInput(attrs={'class':'inp'}),
			'invoiceNo': forms.TextInput(attrs={'class':'inp'}),
			'value': forms.TextInput(attrs={'class':'inp'}),
			'gst_rate': forms.CheckboxInput(attrs={'class':'inp'}),
			'cgst': forms.TextInput(attrs={'class':'inp'}),
			'sgst': forms.TextInput(attrs={'class':'inp'}),
			'igst': forms.TextInput(attrs={'class':'inp'}),
			'recipent_gstin': forms.TextInput(attrs={'class':'inp'}),
			'due_date': forms.DateInput(attrs={'class':'inp'}),
			'status': forms.RadioSelect(attrs={'class':'inp'}),
		}