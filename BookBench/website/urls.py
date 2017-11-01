from django.conf.urls import url
from views import *

urlpatterns = [
	url(r'^login/$', login_view),
	url(r'^home/$', home),
	url(r'^logout/$', logout_view),
    # url(r'^projectbackend/', admin.site.urls),
    url(r'^register/$', register_view),
    url(r'^$', main_login_page),
]