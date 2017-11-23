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

@csrf_exempt
@login_required(login_url='')
def view_wishlist(request):
	user = request.user
	if request.method != "POST":
		wishlist_books = Book.objects.filter(userwishlist__user=user).annotate(wish_status = Case(
			When(userwishlist__status='RE',then=Value(0)),
			When(userwishlist__status='CR',then=Value(1)),
			When(userwishlist__status='WR',then=Value(2)),
			default = Value(-1),output_field=IntegerField()))
		# pagination
		wishlist_books = wishlist_books.order_by('ISBN')

		paginator = Paginator(wishlist_books, 10)
		page = request.GET.get('page')
		print("Page: ", page)
		try:
			wishlist_books = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			wishlist_books = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			wishlist_books = paginator.page(paginator.num_pages)
		return render(request, '../templates/wishlist.html', {'wishlist_books':wishlist_books})

	bookISBN = request.POST['bookISBN']
	book = Book.objects.get(ISBN=bookISBN)
	status = request.POST['status']

	userWishList = UserWishlist.objects.filter(user=user,book=book)
	if userWishList:
		if status == "none":
			userWishList.delete()
			return HttpResponse(1)

		else:
			userWishList[0].status = status
			userWishList[0].save()
			return HttpResponse(2)
	else:
		if status!="none":
			userWishList = UserWishlist.objects.create(user=user, book=book, status=status)
			userWishList.save()
			return HttpResponse(3)
		else:
			return HttpResponse(0)
	

@csrf_exempt
@login_required(login_url='')
def view_owned_books(request):
	user = request.user
	if request.method != "POST":
		user_owned_books = Book.objects.filter(userownedbook__user=user).annotate(owned_status = Case(
			When(userownedbook__status='AV',then=Value(0)),
			When(userownedbook__status='UA',then=Value(1)),
			When(userownedbook__status='LE',then=Value(2)),
			default = Value(-1),output_field=IntegerField()))

		user_owned_books = user_owned_books.order_by('ISBN')
		# pagination
		paginator = Paginator(user_owned_books, 10)
		page = request.GET.get('page')
		print("Page: ", page)
		try:
			user_owned_books = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			user_owned_books = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			user_owned_books = paginator.page(paginator.num_pages)
		return render(request, '../templates/owned_books.html', {'user_owned_books':user_owned_books})

	bookISBN = request.POST['bookISBN']
	book = Book.objects.get(ISBN=bookISBN)
	status = request.POST['status']

	userOwnedBook = UserOwnedBook.objects.filter(user=user,book=book)
	if userOwnedBook:
		if status == "none":
			userOwnedBook.delete()
			return HttpResponse(1)
		else:
			userOwnedBook[0].status = status
			userOwnedBook[0].save()
			return HttpResponse(2)
	else:
		if status != "none":
			userOwnedBook = UserOwnedBook.objects.create(user=user, book=book, status=status)
			userOwnedBook.save()
			return HttpResponse(3)
		else:
			return HttpResponse(0)			