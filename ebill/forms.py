from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Bill
#from .backends import TaxpayerBackend, OfficialBackend
#import re
class DateInput(forms.DateInput):
	input_type = 'date'
class BillForm(forms.ModelForm):
	transaction = (
		('inward', 'inward'),
		('inward', 'outward'),
	)
	sub = (
		('supply', 'supply'),
		('fair', 'fair'),
		('other', 'other'),
	)
	tr_type = forms.TypedChoiceField(choices=transaction, coerce=str, label='Transaction type')
	sub_type = forms.TypedChoiceField(choices=sub, coerce=str, label='SUB-type')
	validFrom = forms.DateField(label='Valid from', help_text="yyyy-mm-dd", widget=forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}))
	validTo = forms.DateField(label='Valid to', help_text="yyyy-mm-dd", widget=forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}))
	generator_gstin = forms.CharField(max_length=14, label='GSTIN', widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	from_name = forms.CharField(max_length=200, label='Name')
	from_address = forms.CharField(max_length=200, label='Address')
	from_pin = forms.IntegerField(label='PIN',widget=forms.TextInput())
	recipent_gstin = forms.CharField(max_length=14, label='GSTIN', widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	to_name = forms.CharField(max_length=200, label='Name')
	to_address = forms.CharField(max_length=200, label='Address')
	to_pin = forms.IntegerField(label='PIN',widget=forms.TextInput())
	product_name = forms.CharField(max_length=200, label='Product name')
	hsn = forms.CharField(label='HSN')
	value = forms.DecimalField(max_digits=50,decimal_places=2, label='Value of goods',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	tax = (
		(0,'0'),
		(5,'5'),
		(12,'12'),
		(18,'18'),
		(28,'28'),
	)
	tax_rate = forms.TypedChoiceField(choices=tax, label='Tax rate', coerce=int)
	tax_amt = forms.DecimalField(max_digits=50, decimal_places=2, label='Tax amount',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	cgst = forms.DecimalField(max_digits=50, decimal_places=2, label='CGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	sgst = forms.DecimalField(max_digits=50, decimal_places=2, label='SGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	igst = forms.DecimalField(max_digits=50, decimal_places=2, label='IGST',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	transportNo = forms.CharField(max_length=20, label='Transport No.')
	distance = forms.DecimalField(max_digits=10, decimal_places=3, label='Distance',widget=forms.TextInput(attrs={'placeholder':'0.000'}))
	class Meta:
		model = Bill
		fields = ['tr_type', 'sub_type', 'validFrom', 'validTo', 'generator_gstin', 'from_name', 'from_address', 'from_pin', 'recipent_gstin', 'to_name', 'to_address', 'to_pin', 'product_name', 
		'hsn', 'value', 'tax_rate', 'tax_amt', 'cgst', 'sgst', 'igst', 'transportNo', 'distance']
		widgets = {
			'tr_type': forms.CheckboxInput(),
			'sub_type': forms.CheckboxInput(),
			'validFrom': DateInput(),
			'validTo': DateInput(),
			'generator_gstin': forms.TextInput(),
			'from_name': forms.TextInput(),
			'from_address': forms.TextInput(),
			'from_pin': forms.TextInput(),
			'recipent_gstin': forms.TextInput(),
			'to_name': forms.TextInput(),
			'to_address': forms.TextInput(),
			'to_pin': forms.TextInput(),
			'product_name': forms.TextInput(),
			'hsn': forms.TextInput(),
			'value': forms.TextInput(),
			'tax_rate': forms.CheckboxInput(),
			'tax_amt': forms.TextInput(),
			'cgst': forms.TextInput(),
			'sgst': forms.TextInput(),
			'igst': forms.TextInput(),
			'transportNo': forms.TextInput(),
			'distance': forms.TextInput(),
		}