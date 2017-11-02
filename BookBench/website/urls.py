from django.conf.urls import url
from views import *

urlpatterns = [
	url(r'^login/$', login_view, name='login_view'),
	url(r'^home/$', home_page, name='home_page'),
	url(r'^logout/$', logout_view, name='logout_view'),
    # url(r'^projectbackend/', admin.site.urls),
    url(r'^register/$', register_view, name='register'),
    url(r'^$', main_login_page, name='main_login_page'),
]