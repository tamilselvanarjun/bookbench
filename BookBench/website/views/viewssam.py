from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from ..models import * # User, Book, Author, Publications, Genre, Review, Report, UserOwnedBook, UserWishList, Review_is_helpful
from ..forms import *
from . import *


# The registration page
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

			messages.add_message(request, messages.SUCCESS, 'Successfully Registered!')
			return HttpResponseRedirect(reverse("main_login_page"))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse("main_login_page"))
		normal_user_form = NormalUserForm()

	return render(request, 'register.html', {'normal_user_form':normal_user_form, 'registered':registered})


# The registration page for admins
def register_admin_view(request):

	registered = False
	# This is the main register page
	if request.method == "POST":
		admin_user_form = AdminUserForm(data=request.POST)

		if admin_user_form.is_valid():
			admin_user = admin_user_form.save()
			admin_user.set_password(admin_user.password)
			admin_user.set_status(admin_user.status)
			admin_user.save()

			registered = True

			messages.add_message(request, messages.ERROR, 'Successfully Registered!')
			return HttpResponseRedirect(reverse("main_login_page"))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse("main_login_page"))
		admin_user_form = AdminUserForm()

	return render(request, 'register_special.html', {'admin_user_form':admin_user_form, 'registered':registered})






# Define the home page
def home_page(request):
	# whatever request, just check if we are in
	if request.method == "GET":
		# check for user
		user = request.user
		if user.is_authenticated():
			# user is authenticated, show stuff here
			return render(request, '../templates/homepage.html', {'user': user})
		else:
			messages.add_message(request, messages.ERROR, 'Login first')
			return HttpResponseRedirect(reverse("main_login_page"))
	else:
		return HttpResponseRedirect(reverse("main_login_page"))
