from django import forms
from django.contrib.auth.models import User
from .models import * 

USER_STATUS_CHOICES = (	
	('AD', 'Admin'),
	('MO', 'Moderator'),
)

class NormalUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'pass','placeholder':'Password','required':''}))

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password'}
		widgets = {
			'first_name': forms.TextInput(attrs = {'class':'user','placeholder':'First Name','required':''}),
			'last_name': forms.TextInput(attrs = {'class':'user','placeholder':'Last Name','required':''}),
			'email': forms.TextInput(attrs = {'class':'user','placeholder':'E-mail','required':''})
		}

class AdminUserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	status = forms.CharField(label = 'Status', widget = forms.Select(choices = USER_STATUS_CHOICES))

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password', 'status'}


class UserLoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'pass','placeholder':'Password','required':''}))
	class Meta:
		model = User
		fields = ['email', 'password']
		widgets = {
			'email': forms.TextInput(attrs = {'class':'user','placeholder':'E-mail','required':''})
		}

class AddBooksForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['ISBN', 'name', 'description', 'authors', 'genres', 'publication']

class AddAuthorsForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['name']

class AddPublicationsForm(forms.ModelForm):
	class Meta:
		model = Publications
		fields = ['name']

class AddGenresForm(forms.ModelForm):
	class Meta:
		model = Genre
		fields = ['name']
