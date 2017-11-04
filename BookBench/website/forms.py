from django import forms
from django.contrib.auth.models import User
from .models import * 

USER_STATUS_CHOICES = (	
	('AD', 'Admin'),
	('MO', 'Moderator'),
)

class NormalUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password'}

class AdminUserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	status = forms.CharField(label = 'Status', widget = forms.Select(choices = USER_STATUS_CHOICES))

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password', 'status'}


class UserLoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ['email', 'password']
