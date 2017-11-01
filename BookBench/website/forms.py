from django import forms
from django.contrib.auth.models import User
from .models import * # User, Book, Author, Publications, Genre, Review, Report, UserOwnedBook, UserWishList, Review_is_helpful

class NormalUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = {'first_name', 'last_name', 'email', 'password'}
