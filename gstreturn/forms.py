from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from invoice.models import Invoice, Return1
class ReturnForm(forms.ModelForm):
	name = forms.CharField(max_length=200, label='Name',widget=forms.TextInput(attrs={'placeholder':'Your name'}))
	gstin = forms.CharField(max_length=200, label='GSTIN',widget=forms.TextInput(attrs={'placeholder':'14 character GSTIN'}))
	from_date = forms.DateField(label='Valid from',widget=forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}))
	to_date = forms.DateField(label='Valid to',widget=forms.DateInput(attrs={'placeholder':'yyyy-mm-dd'}))
	class Meta:
		model = Return1
		fields = ['name', 'gstin', 'from_date', 'to_date']
		widgets = {
			'name': forms.TextInput(attrs={'class':'inp'}),
			'gstin': forms.TextInput(attrs={'class':'inp'}),
			'from_date': forms.DateInput(),
			'to_date': forms.DateInput(),
		}