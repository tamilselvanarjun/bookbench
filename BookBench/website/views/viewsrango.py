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
from django.db.models import *
from ..forms import *
import json


# Define the first home login page
def main_login_page(request):
	# This is the main login page
	if request.method == "GET":
		# check for user
		user=request.user
		if user.is_authenticated():
			genres = user.preferred_genres.all()
			# ctx = {}
			# if genres:
			# 	count = 0
			# 	for g in genres:
			# 		ctx[str(count)] = g.name
			# 		ctx['books'+str(count)] = 
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

	if request.method!="GET":
		return HttpResponseRedirect(reverse("home_page"))

	# check if we actually searched
	if request.GET.get('search') is None:
		return render(request, '../templates/advanced_search.html', {
				'user': user
		})
	else:
		qs = Book.objects.none()
		query = request.GET.get('query')
		sortCondition = request.GET.get("sortCondition")
		params = request.GET.getlist('parameters')

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

		qs = qs.annotate(score=Coalesce(Sum('review__rating'), 0))

		#################################

		qs = qs.annotate(wish_status = Case(
			When(Q(userwishlist__status='RE')&Q(userwishlist__user=user),then=Value(0)),
			When(Q(userwishlist__status='CR')&Q(userwishlist__user=user),then=Value(1)),
			When(Q(userwishlist__status='WR')&Q(userwishlist__user=user),then=Value(2)),
			default = Value(-1),output_field=IntegerField()))

		qs = qs.annotate(owned_status = Sum(Case(
			When(Q(userownedbook__status='AV')&Q(userownedbook__user=user),then=Value(0)),
			When(Q(userownedbook__status='UA')&Q(userownedbook__user=user),then=Value(1)),
			When(Q(userownedbook__status='LE')&Q(userownedbook__user=user),then=Value(2)),
			default = Value(-1),output_field=IntegerField())))

		#################################

		# order the books
		if "name" == sortCondition:
			qs = qs.order_by('name')
		else:
			qs = qs.order_by('-score')
		qs = qs.distinct()
		

		# pagination
		paginator = Paginator(qs, 10)
		page = request.GET.get('page')
		print("Page: ", page)
		try:
			qs = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			qs = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			qs = paginator.page(paginator.num_pages)

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

	# get all the reviews
	reviews = Review.objects.filter(review_book=book)

	# get the reviews where user hasn't rated
	reviews_user_not_rated = reviews.exclude(review_is_helpful__review_user=user).annotate(helpful= \
								Sum(Case(When(review_is_helpful__is_helpful=True, then=Value(1)), default=Value(0), \
								output_field=IntegerField())))

	reviews_user_rated = reviews.filter(review_is_helpful__review_user=user)

	reviews_user_rated = Review_is_helpful.objects.prefetch_related(Prefetch('review_user', queryset=reviews_user_rated))\
					.filter(on_review__review_book=book).filter(review_user=user)\
					.annotate(helpful=Sum(Case(When(on_review__review_is_helpful__is_helpful=True, then=Value(1)), \
					default=Value(0), output_field=IntegerField())))

	reviews = reviews.annotate(helpful=Sum(Case(When(review_is_helpful__is_helpful=True, then=Value(1)), default=Value(0), \
				output_field=IntegerField())))

	##############################################
	userWishList = UserWishlist.objects.filter(user=user,book=book)
	if(userWishList):
		ctx['wishlist'] = userWishList[0].status
	else:
		ctx['wishlist'] = "none"

	userOwnedBook = UserOwnedBook.objects.filter(user=user,book=book)
	if(userOwnedBook):
		ctx['owned'] = userOwnedBook[0].status
	else:
		ctx['owned'] = "none"
	##############################################

	# reviews = reviews.annotate(my_help)
	if(reviews.count() > 0):
		ctx['avg_rating'] = reviews.aggregate(Avg("rating"))["rating__avg"]
		ctx['reviews'] = reviews
		ctx['reviews_user_rated'] = reviews_user_rated
		ctx['reviews_user_not_rated'] = reviews_user_not_rated

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


@login_required
def genre_details(request, ID):
	if request.method!="GET":
		return HttpResponseRedirect(reverse('home_page'))
	else:
		page = request.GET.get('page')
		genre = Genre.objects.get(ID=ID)
		books = genre.book_set.all()
		paginator = Paginator(books, 10)
		try: 
			b = paginator.page(page)
		except PageNotAnInteger:
			b = paginator.page(1)
		except EmptyPage:
			b = paginator.page(paginator.num_pages)

		ctx = {
			'genre': genre,
			'books': b,
		}

		return render(request, '../templates/genre_details.html', ctx)


@login_required
def author_details(request, ID):
	if request.method!="GET":
		return HttpResponseRedirect(reverse('home_page'))
	else:
		page = request.GET.get('page')
		author = Author.objects.get(ID=ID)
		books = author.book_set.all()
		paginator = Paginator(books, 10)
		try: 
			b = paginator.page(page)
		except PageNotAnInteger:
			b = paginator.page(1)
		except EmptyPage:
			b = paginator.page(paginator.num_pages)

		ctx = {
			'author': author,
			'books': b,
		}

		return render(request, '../templates/author_details.html', ctx)


@login_required
def publication_details(request, ID):
	if request.method!="GET":
		return HttpResponseRedirect(reverse('home_page'))
	else:
		page = request.GET.get('page')
		publ = Publications.objects.get(ID=ID)
		books = publ.book_set.all()
		paginator = Paginator(books, 10)
		try: 
			b = paginator.page(page)
		except PageNotAnInteger:
			b = paginator.page(1)
		except EmptyPage:
			b = paginator.page(paginator.num_pages)

		ctx = {
			'pub': publ,
			'books': b,
		}

		return render(request, '../templates/publication_details.html', ctx)

# get all users who have this book
@login_required
def userbook(request, ISBN):
	user = request.user
	book = Book.objects.get(ISBN=ISBN)
	userbooks = book.userownedbook_set.all()

	ctx = {
		'user': user,
		'book': book,
		'userbooks': userbooks,
	}

	return render(request, '../templates/user_book.html', ctx)


@login_required
def user_details(request, ID):
	me = request.user
	user_ = User.objects.get(ID=ID)

	ctx = {
		'me': me,
		'user': user_,
	}

	return render(request, '../templates/user_details.html', ctx)

@csrf_exempt
@login_required
def report_user_api(request):
	print(request.POST)
	ID = request.POST['ID']
	text = request.POST['text']
	user_ = User.objects.get(ID=ID)
	me = request.user
	userreport = ReportUser.objects.get_or_create(on_user=user_, report_user=me)[0]
	userreport.text = text
	userreport.save()
	return HttpResponse(1)

@login_required
def banned_users(request):
	user = request.user
	banned = User.objects.filter(active=False)

	ctx = {
		'user': user,
		'banned' : banned,
	}

	return render(request, '../templates/banned_users.html', ctx)


@csrf_exempt
@login_required
def unban_banned_user(request):
	user = request.user
	ID = request.POST['ID']
	banned_user = User.objects.get(ID=ID)
	banned_user.active = True
	banned_user.save()
	return HttpResponse(1)