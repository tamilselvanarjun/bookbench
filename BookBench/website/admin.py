# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publications)

admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(UserOwnedBook)
admin.site.register(UserWishlist)
admin.site.register(Review_is_helpful)
