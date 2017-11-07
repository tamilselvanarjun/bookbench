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
	user = request.user
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
		# check for image
		img = request.FILES['image']
		user.profile_picture = img
		user.save()
		return HttpResponseRedirect(reverse("main_login_page"))


@login_required(login_url='')
def add_books(request):
	if request.method == "GET":
		add_books_form = AddBooksForm()
		return render(request, '../templates/add_books.html', {'add_books_form':add_books_form})
	else:
		add_books_form = AddBooksForm(data=request.POST)
		add_books = add_books_form.save()
		add_books.save()
		messages.add_message(request, messages.ERROR, 'Successfully Added new Book!')
		return HttpResponseRedirect(reverse("add_books"))



@login_required(login_url='')
def add_publications(request):
	if request.method == "GET":
		add_publications_form = AddPublicationsForm()
		return render(request, '../templates/add_books.html', {'add_publications_form':add_publications_form})
	else:
		add_publications_form = AddPublicationsForm(data=request.POST)
		add_publications = add_publications_form.save()
		add_publications.save()
		messages.add_message(request, messages.ERROR, 'Successfully Added new Publication!')
		return HttpResponseRedirect(reverse("add_publications"))



@login_required(login_url='')
def add_authors(request):
	
	if request.method == "GET":
		add_authors_form = AddAuthorsForm()
		return render(request, '../templates/add_books.html', {'add_authors_form':add_authors_form})
	else:
		add_authors_form = AddAuthorsForm(data=request.POST)
		add_authors = add_authors_form.save()
		add_authors.save()
		messages.add_message(request, messages.ERROR, 'Successfully Added new Author!')
		return HttpResponseRedirect(reverse("add_authors"))


@login_required(login_url='')
def add_genres(request):
	
	if request.method == "GET":
		add_genres_form = AddGenresForm()
		return render(request, '../templates/add_books.html', {'add_genres_form':add_genres_form})
	else:
		add_genres_form = AddGenresForm(data=request.POST)
		add_genres = add_genres_form.save()
		add_genres.save()
		messages.add_message(request, messages.ERROR, 'Successfully Added new Genre!')
		return HttpResponseRedirect(reverse("add_genres"))

@login_required(login_url='')
def add_moderators(request):
	user = request.user
	if request.method == "GET":
		return render(request, '../templates/add_moderators.html', {
				'user': user
		})
	else:
		user_list = User.objects.none()
		query = request.POST.get('query')
		params = request.POST.getlist('parameters')

		print(query, params)
		search_query = query.split()
		if "name" in params:
			print(params)
			for ind_query in search_query:
				user_list = user_list | (User.objects.filter(first_name__icontains=ind_query))
				user_list = user_list | (User.objects.filter(last_name__icontains=ind_query))
		if "email" in params:
			print(params)
			for ind_query in search_query:
				user_list = user_list | (User.objects.filter(email__icontains=ind_query))

		user_list = user_list.distinct()

		context = {
			'user': user,
			'user_list': user_list,
			'results': True,
		}

		print(context)
		return render(request, '../templates/add_moderators.html', context)


# toggle the user status
@csrf_exempt
@login_required(login_url='')
def mod_toggle_api(request):
	if request.method != "POST":
		return HttpResponse(-1)
	
	user = request.user
	uID = request.POST['uID']
	target = request.POST['response']
	user_target = User.objects.get(ID=uID)
	count = -1

	if user_target.status == 'MO' and target == 'normie':
		print "moderator is changing"
		user_target.status = 'US'
		count = 0
	elif user_target.status == 'US' and target == 'mod':
		print "user is changing"
		user_target.status = 'MO'
		count = 1
	else:
		count = 2

	user_target.save()

	return HttpResponse(count)


@csrf_exempt
@login_required(login_url='')
def delete_user_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		delete_userID = request.POST['deleteID']
		delete_user = User.objects.get(ID=delete_userID)
		delete_user.active = False
		delete_user.save()
		return HttpResponse(1)

@csrf_exempt
@login_required(login_url='')
def delete_report_user_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		print(request.POST)
		reportID = request.POST['reportID']
		report = ReportUser.objects.get(ID=reportID)
		report.delete()
		return HttpResponse(1)

@login_required(login_url='')
def check_report_user_view(request):
	user = request.user
	if request.method == "GET":
		reports = ReportUser.objects.all()
		return render(request, '../templates/check_report_user.html', {'user' : user, 'reports' : reports, 'results' : True})
