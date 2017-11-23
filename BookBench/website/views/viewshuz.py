# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from ..models import * # User, Book, Author, Publications, Genre, Review, Report, UserOwnedBook, UserWishList, Review_is_helpful
from ..forms import *
from . import *

# Moderator Reports
@login_required(login_url='')
def check_report_view(request):
	user = request.user
	if request.method == "GET":
		reports = Report.objects.all()
		return render(request, '../templates/check_report.html', {'user' : user, 'reports' : reports, 'results' : True})

@csrf_exempt
@login_required(login_url='')
def delete_review_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		reviewID = request.POST['reviewID']
		review = Review.objects.get(ID=reviewID)
		review.delete()
		return HttpResponse(1)

@csrf_exempt
@login_required(login_url='')
def delete_report_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		print(request.POST)
		reportID = request.POST['reportID']
		report = Report.objects.get(ID=reportID)
		report.delete()
		return HttpResponse(1)

@csrf_exempt
@login_required(login_url='')
def add_report_api(request):
	if request.method != "POST":
		return HttpResponse(-1)
	else:
		text = request.POST['text']
		reviewID = request.POST['reviewID']
		
		# get review and user
		review = Review.objects.get(ID=reviewID)
		user = request.user

		try:
			# update
			report = Report.objects.get(report_user=user, on_review=review)
			report.text = text
			report.save()
			return HttpResponse(1)
		except:
			report = Report.objects.create(report_user=user, on_review=review, text=text)
			report.save()
			return HttpResponse(0)


@csrf_exempt
@login_required(login_url='')
def messages(request):
	if request.method != "POST":
		user = request.user
		inbox = Message.objects.filter(receiver=user)
		outbox = Message.objects.filter(sender=user)
		return render(request, '../templates/messages.html', {'user' : user, 'outbox' : outbox, 'inbox' : inbox, 'results' : True})
		

@csrf_exempt
@login_required(login_url='')
def add_message_api(request):
	if request.method != "POST":
		return HttpResponse(-1)
	else:

		user = request.user
		email_id = request.POST['email_id']
		message_text = request.POST['message_text']
		receiver = User.objects.get(email=email_id)
		message = Message.objects.create(sender=user, receiver=receiver, message_text=message_text)
		message.save()
		return HttpResponse(0)