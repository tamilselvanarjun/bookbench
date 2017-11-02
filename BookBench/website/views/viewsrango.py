# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from ..forms import *


# Define the first home login page
def main_login_page(request):
	# This is the main login page
	if request.method == "GET":
		# check for user
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse("home_page"))
		else:
			form = UserLoginForm()
			return render(request, '../templates/main_login_page.html', {'form' : form})
	# POST request
	else:
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("home_page"))
		else:
			messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
			return HttpResponseRedirect(reverse(("main_login_page")))


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