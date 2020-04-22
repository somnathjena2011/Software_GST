from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
#from .backends import TaxpayerBackend, OfficialBackend
#import re

class CardForm(forms.Form):
	gstin = forms.CharField(max_length=14, label='GSTIN',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	name = forms.CharField(max_length=200, label='Name', widget=forms.TextInput(attrs={'placeholder':'Name of Cardholder'}))
	expiry = forms.DateField(label='Expiry date', widget=forms.DateInput(attrs={'placeholder':'mm/yy'}))
	cvv = forms.IntegerField(label='CVV', widget=forms.TextInput(attrs={'placeholder':'000'}))
	amount = forms.DecimalField(max_digits=50, decimal_places=2, label='Amount',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	class Meta:
		#model = Invoice
		fields = ['gstin', 'name', 'expiry', 'cvv', 'amount']

class NetForm(forms.Form):
	gstin = forms.CharField(max_length=14, label='GSTIN',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	account = forms.CharField(max_length=12, label='Your Bank Account No.',widget=forms.TextInput(attrs={'placeholder':'Account No.'}))
	ifsc = forms.CharField(max_length=12, label='IFSC code of your bank branch',widget=forms.TextInput(attrs={'placeholder':'IFSC'}))
	amount = forms.DecimalField(max_digits=50, decimal_places=2, label='Amount to pay',widget=forms.TextInput(attrs={'placeholder':'0.00'}))
	class Meta:
		#model = Invoice
		fields = ['gstin', 'account','ifsc','amount']
		widgets = {
			'gstin': forms.TextInput(attrs={'class':'inp'}),
			'account': forms.TextInput(attrs={'class':'inp'}),
			'ifsc':forms.TextInput(attrs={'class':'inp'}),
			'amount':forms.TextInput(attrs={'class':'inp'}),
		}