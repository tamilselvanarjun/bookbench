from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

USER_STATUS = (	
	('AD', 'Admin'),
	('MO', 'Moderator'),
	('US', 'User'),
) 

BOOK_LEND_STATUS = (
	('AV', 'Available'),
	('UA', 'Unavailable'),
	('LE', 'Lent')
)

BOOK_READ_STATUS = (
	('RE', 'Read'),
	('CR', 'Currently Reading'),
	('WR', 'Want to read')
)

RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class BookBenchUserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
	
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault("is_superuser", True)
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must be true.")

		return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser):
	'''
	Store the user model in this class.
	'''
	objects = BookBenchUserManager()

	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

	ID = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=254, unique=True)
	# calculate sha256sum
	# password = models.CharField(max_length=64)
	longitude = models.DecimalField(default=-1, max_digits=13, decimal_places=10)
	langitude = models.DecimalField(default=-1, max_digits=13, decimal_places=10)
	status = models.CharField(max_length=2, choices=USER_STATUS, default='US')

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name



class Book(models.Model):
	'''
	Book details
	'''
	ISBN = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000)

	# list of authors, publications, genres
	authors = models.ManyToManyField("Author")
	genres = models.ManyToManyField("Genre")
	publication = models.ForeignKey("Publications", on_delete=models.CASCADE)


class Author(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)


class Publications(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)


class Genre(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)


class Review(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(auto_now=True)
	rating = models.IntegerField(default=1, choices=RATINGS)

	# details like user who reviewed and book on which review 
	# is given
	review_user = models.ForeignKey("User", on_delete=models.CASCADE)
	review_book = models.ForeignKey("Book", on_delete=models.CASCADE)


class Report(models.Model):
	ID = models.AutoField(primary_key=True)
	text = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(auto_now=True)	

	# user who reported and the review on which report was given
	report_user = models.ForeignKey("User", on_delete=models.CASCADE)
	on_review = models.ForeignKey("Review", on_delete=models.CASCADE)


class UserOwnedBook(models.Model):
	ID = models.AutoField(primary_key=True)
	user = models.ForeignKey('User', on_delete=models.CASCADE)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)
	status = models.CharField(max_length=2, choices=BOOK_LEND_STATUS, default='AV')


class UserWishlist(models.Model):
	ID = models.AutoField(primary_key=True)
	user = models.ForeignKey('User', on_delete=models.CASCADE)
	book = models.ForeignKey('Book', on_delete=models.CASCADE)
	status = models.CharField(max_length=2, choices=BOOK_READ_STATUS, default='WR')	


class Review_is_helpful(models.Model):
	ID = models.AutoField(primary_key=True)
	is_helpful = models.BooleanField()

	# associated user who gave the review, and the review itself
	review_user = models.ForeignKey('User', on_delete=models.CASCADE)
	on_review = models.ForeignKey('Review', on_delete=models.CASCADE)
