from django import forms
from django.forms import ModelForm
from .models import users,stock

class stockform(ModelForm):
	class Meta:
		model=stock
		fields=['stock_name','stock_data']

class loginform(ModelForm):
	class Meta:
		password = forms.CharField(widget=forms.PasswordInput)
		model=users
		widgets = {
            'password': forms.PasswordInput(),
        }
		fields=['username','password']

class registerform(ModelForm):
	class Meta:
		password = forms.CharField(widget=forms.PasswordInput)
		model=users
		widgets = {
            'password': forms.PasswordInput(),
        }
		fields=['name','username','email','password']
