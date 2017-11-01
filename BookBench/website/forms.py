from django import forms
from .models import *

class UserLoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ['email', 'password']
