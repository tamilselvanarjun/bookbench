from django import forms
from django.contrib.auth.models import User
from .models import * 

USER_STATUS_CHOICES = (	
	('AD', 'Admin'),
	('MO', 'Moderator'),
)

class NormalUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'Password','required':''}))

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password'}
		
		widgets = {
			'first_name': forms.TextInput(attrs = {'placeholder':'First Name','required':''}),
			'last_name': forms.TextInput(attrs = {'placeholder':'Last Name','required':''}),
			'email': forms.TextInput(attrs = {'placeholder':'E-mail','required':''})
		}

class AdminUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'Password','required':''}))
	status = forms.CharField(label = 'Status', widget = forms.Select(choices = USER_STATUS_CHOICES))

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password', 'status'}

		widgets = {
			'first_name': forms.TextInput(attrs = {'placeholder':'First Name','required':''}),
			'last_name': forms.TextInput(attrs = {'placeholder':'Last Name','required':''}),
			'email': forms.TextInput(attrs = {'placeholder':'E-mail','required':''})
		}



class UserLoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder':'Password','required':''}))
	class Meta:
		model = User
		fields = ['email', 'password']
		
		widgets = {
			'email': forms.TextInput(attrs = {'placeholder':'E-mail','required':''})
		}

class AddBooksForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddBooksForm,self).__init__(*args, **kwargs)
		
		fields__ = ['ISBN', 'name', 'description', 'authors', 'genres', 'publication']
		
		for f in fields__:
			self.fields[f].label = ''

	class Meta:
		model = Book
		fields = ['ISBN', 'name', 'description', 'authors', 'genres', 'publication']
		widgets = {
			'ISBN': forms.TextInput(attrs = {'placeholder':'ISBN','required':''}),
			'name': forms.TextInput(attrs = {'placeholder':'Name','required':''}),
			'description': forms.TextInput(attrs = {'placeholder':'Description','required':''}),
			'authors': forms.TextInput(attrs = {'placeholder':'Authors','required':''}),
			'genres': forms.TextInput(attrs = {'placeholder':'Genres','required':''}),
			'publication': forms.TextInput(attrs = {'placeholder':'Publication','required':''})
		}


class AddAuthorsForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddAuthorsForm,self).__init__(*args, **kwargs)
		
		fields__ = ['name']
		
		for f in fields__:
			self.fields[f].label = ''
	class Meta:
		model = Author
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs = {'placeholder':'Name','required':''})
		}


class AddPublicationsForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddPublicationsForm,self).__init__(*args, **kwargs)
		
		fields__ = ['name']
		
		for f in fields__:
			self.fields[f].label = ''
	class Meta:
		model = Publications
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs = {'placeholder':'Name','required':''})
		}


class AddGenresForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddGenresForm,self).__init__(*args, **kwargs)
		
		fields__ = ['name']
		
		for f in fields__:
			self.fields[f].label = ''
	class Meta:
		model = Genre
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs = {'placeholder':'Name','required':''})
		}

