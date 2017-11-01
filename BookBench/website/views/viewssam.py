from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from ..models import * # User, Book, Author, Publications, Genre, Review, Report, UserOwnedBook, UserWishList, Review_is_helpful
from ..forms import *

def register_view(request):

	registered = False
	# This is the main register page
	if request.method == "POST":
		normal_user_form = NormalUserForm(data=request.POST)

		if normal_user_form.is_valid():
			normal_user = normal_user_form.save()
			normal_user.set_password(normal_user.password)
			normal_user.save()

			registered = True
	else:
		normal_user_form = NormalUserForm()

	return render(request, 'register.html', {'normal_user_form':normal_user_form, 'registered':registered})
