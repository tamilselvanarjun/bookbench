from django.conf.urls import url
from views import *

urlpatterns = [
	url(r'^login/$', login_view, name='login_view'),
	url(r'^home/$', home_page, name='home_page'),
	url(r'^logout/$', logout_view, name='logout_view'),
    # url(r'^projectbackend/', admin.site.urls),
    url(r'^register/$', register_view, name='register'),
    url(r'^registeradmin/$', register_admin_view, name='register_admin_view'),
    url(r'^prefgenres/$', preferred_genres, name='preferred_genres'),
    url(r'^search/$', advanced_search, name='advanced_search'),
    url(r'^book/(?P<ISBN>[a-zA-Z0-9\-]+)$', book_details, name='book_details'),
    url(r'^$', main_login_page, name='main_login_page'),
]