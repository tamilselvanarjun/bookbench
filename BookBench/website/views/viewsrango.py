# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg
from ..forms import *
import json


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
		user = authenticate(email=email, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("home_page"))
		else:
			messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
			return HttpResponseRedirect(reverse(("main_login_page")))


# # Define the home page
# def home_page(request):
# 	# whatever request, just check if we are in
# 	if request.method == "GET":
# 		# check for user
# 		user = request.user
# 		if user.is_authenticated():
# 			# user is authenticated, show stuff here
# 			return render(request, '../templates/homepage.html', {'user': user})
# 		else:
# 			messages.add_message(request, messages.ERROR, 'Login first')
# 			return HttpResponseRedirect(reverse("main_login_page"))
# 	else:
# 		return HttpResponseRedirect(reverse("main_login_page"))

@login_required(login_url='')
def preferred_genres(request):

	# here, we just display the form
	user = request.user
	if request.method == "GET":
		genres = Genre.objects.all()
		user = request.user

		return render(request, '../templates/preferred_genres.html', {
				'user' : user,
				'genres' : genres,
			})
	# process the form
	else:
		genre_list = request.POST.getlist('genres')
		user.preferred_genres.remove()
		for g in genre_list:
			query = Genre.objects.get(name=g)
			user.preferred_genres.add(query)
		user.save()
		messages.add_message(request, messages.SUCCESS, 'Preferences updated!')
		return HttpResponseRedirect(reverse("home_page"))

## TODO
@login_required(login_url='')
def advanced_search(request):
	user = request.user
	if request.method == "GET":
		return render(request, '../templates/advanced_search.html', {
				'user': user
		})
	else:
		qs = Book.objects.none()
		query = request.POST.get('query')
		params = request.POST.getlist('parameters')
		print(query, params)
		if "name" in params:
			print(params)
			qs = qs | (Book.objects.filter(name__icontains=query))
		if "isbn" in params:
			print(params)
			qs = qs | (Book.objects.filter(ISBN__icontains=query))
		if "description" in params:
			print(params)
			qs = qs | (Book.objects.filter(description__icontains=query))
		if "publications" in params:
			print(params)
			pub = Publications.objects.filter(name__icontains=query)
			qs = qs | (Book.objects.filter(publication__in=pub))
		if "genres" in params:
			print(params)
			genres = Genre.objects.filter(name__icontains=query)
			qs = qs | Book.objects.filter(genres__in=genres)
		if "authors" in params:
			print(params)
			authors = Author.objects.filter(name__icontains=query)
			qs = qs | (Book.objects.filter(authors__in=authors))

		context = {
			'user': user,
			'books': qs.distinct(),
			'results': True,
		}
		print(context)
		return render(request, '../templates/advanced_search.html', context)


@login_required(login_url='')
def book_details(request, ISBN):
	user = request.user
	book = Book.objects.get(ISBN=ISBN)
	ctx = {'user': user, 'book': book}
	# get the average rating
	reviews = Review.objects.filter(review_book=book)
	if(reviews.count() > 0):
		ctx['avg_rating'] = reviews.aggregate(Avg("rating"))["rating__avg"]
		ctx['reviews'] = reviews

	# get review for the user
	my_review = reviews.filter(review_user=user)
	if my_review.count() > 0:
		my_review = my_review[0]
		ctx['my_rating'] = my_review.rating
		ctx['my_review'] = my_review.text

	return render(request, '../templates/book_details.html', ctx)


@csrf_exempt
@login_required(login_url='')
def update_rating_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		ctx={
			'avg_rating':'',
		}
		user = request.user
		isbn = request.POST.get('ISBN')
		book = Book.objects.get(ISBN=isbn)
		user_rating = request.POST.get("my_rating")
		# create a new review object or get one
		try:
			review = Review.objects.get(review_user=user, review_book=book)
		except:
			review = Review.objects.create(review_user=user, review_book=book)
		review.rating = user_rating
		review.save()

		# return the new average rating 
		review = Review.objects.filter(review_book=book)
		if review.count() > 0:
			ctx['avg_rating'] = review.aggregate(Avg("rating"))['rating__avg']
		return HttpResponse(json.dumps(ctx))


@csrf_exempt
@login_required(login_url='')
def update_review_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	else:
		user = request.user
		isbn = request.POST.get('ISBN')
		book = Book.objects.get(ISBN=isbn)
		text = request.POST.get("my_review")
		# create a new review object or get one
		try:
			review = Review.objects.get(review_user=user, review_book=book)
		except:
			review = Review.objects.create(review_user=user, review_book=book)
		review.text = text
		review.save()

		# return 1 or 0
		return HttpResponse(1)

@csrf_exempt
@login_required(login_url='')
def update_location_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	user = request.user
	lon = request.POST['lon']
	lat = request.POST['lat']
	user.longitude = lon
	user.latitude = lat
	user.save()
	return HttpResponse(1)