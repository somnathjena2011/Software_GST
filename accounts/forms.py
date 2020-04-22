from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import User, TaxpayerProfile, OfficialProfile
from .backends import TaxpayerBackend, OfficialBackend
from django.http import HttpResponse
import re
class UserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	last_name = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Your email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Create a strong password'}))
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password']
		widgets = {
			'password': forms.PasswordInput(attrs={'placeholder':'Create a strong password'}),
			'first_name': forms.TextInput(attrs={'placeholder':'First Name'}),
			'last_name': forms.TextInput(attrs={'placeholder':'Last Name'}),
			'email': forms.EmailInput(attrs={'placeholder':'Your email'}),
		}

class TaxpayerProfileForm(forms.ModelForm):
	class Meta:
		model = TaxpayerProfile
		fields = ['aadhar']
		widgets = {
			'aadhar': forms.TextInput(attrs={'placeholder':'12 digit aadhar'}),
		}

class OfficialProfileForm(forms.ModelForm):
	class Meta:
		model = OfficialProfile
		fields = ['aadhar', 'uid']
		widgets = {
			'aadhar': forms.TextInput(attrs={'placeholder':'12 digit aadhar'}),
			'uid': forms.TextInput(attrs={'placeholder':'Your unique ID'}),
		}

class TaxpayerLoginForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'inp'}),
			'password': forms.PasswordInput(attrs={'class':'inp'})
		}

class OfficialLoginForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'inp'}),
			'password': forms.PasswordInput(attrs={'class':'inp'})
		}