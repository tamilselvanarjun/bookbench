# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg, Sum, Count, When, Case, Value, IntegerField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
		sortCondition = request.POST.get("sortCondition")
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

		# order the books
		if "name" == sortCondition:
			qs = qs.order_by('name')
		else:
			qs = qs.annotate(score=Coalesce(Sum('review__rating'), 0)).order_by('-score')

		qs = qs.distinct()

		context = {
			'user': user,
			'books': qs,
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
	reviews = reviews.annotate(helpful=Sum(Case(When(review_is_helpful__is_helpful=True, then=Value(1)), default=Value(0), \
				output_field=IntegerField())))
	# reviews = reviews.annotate(my_help)
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

# update the reviews
@csrf_exempt
@login_required(login_url='')
def update_review_helpful_api(request):
	if request.method!="POST":
		return HttpResponse(-1)
	user = request.user
	reviewID = request.POST['reviewID']
	response = request.POST['response']
	review = Review.objects.get(ID=reviewID)

	try:
		helpful = Review_is_helpful.objects.get(review_user=user, on_review=review)
		if response == "none":
			helpful.delete()
		else:
			if response == "yes":
				helpful.is_helpful = True
			else:
				helpful.is_helpful = False
			helpful.save()
	except:
		if response != "none":
			# make a new one
			helpful = Review_is_helpful.objects.create(review_user=user, on_review=review,is_helpful=False)
			if response == "yes":
				helpful.is_helpful = True
			else:
				helpful.is_helpful = False
			helpful.save()

	count = review.review_is_helpful_set.annotate(helpful=\
				Case(When(is_helpful=True, then=Value(1)), default=Value(0), \
				output_field=IntegerField())).aggregate(Sum('helpful'))['helpful__sum']
	if count is None:
		count = 0

	return HttpResponse(count)




