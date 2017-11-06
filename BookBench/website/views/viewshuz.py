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
