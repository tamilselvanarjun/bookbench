# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Define the first home login page
def main_login_page(request):
	# This is the main login page
	if request.method == "GET":
		# check for user
		user = request.user
		print(user)
		return HttpResponse("1")
