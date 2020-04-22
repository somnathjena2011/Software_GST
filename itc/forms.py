from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
#from .backends import TaxpayerBackend, OfficialBackend
#import re

class ITCForm(forms.Form):
	gstin = forms.CharField(max_length=14, label='GSTIN')
	account = forms.CharField(max_length=12, label='Your Bank Account No.')
	ifsc = forms.CharField(max_length=12, label='IFSC code of your bank branch')
	amount = forms.DecimalField(max_digits=50, decimal_places=2, label='Amount to claim')
	class Meta:
		#model = Invoice
		fields = ['gstin', 'account','ifsc','amount']
		widgets = {
			'gstin': forms.TextInput(attrs={'class':'inp'}),
			'account': forms.TextInput(attrs={'class':'inp'}),
			'ifsc':forms.TextInput(attrs={'class':'inp'}),
			'amount':forms.TextInput(attrs={'class':'inp'}),
		}