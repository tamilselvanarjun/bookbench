# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
@csrf_exempt
def login_view(request):
	if request.method != "POST":
		return HttpResponse(json.dumps({
				'status': -1,
				'error'	: 'Send POST request'
			}))
	else:
		print(request.POST)
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return HttpResponse(json.dumps({
					'status': 1,
					'message': 'Done'
				}))
		else:
			return HttpResponse(json.dumps({
					'status': -1,
					'error'	: 'Invalid credentials!',
				}))

@csrf_exempt
def home(request):
	print(request.user)
	return HttpResponse("Not implemented.")

@csrf_exempt
def logout_view(request):
	print(request.user)
	logout(request)
	return HttpResponse(json.dumps({
			'status':1,
		}))