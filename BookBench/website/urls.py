from django.conf.urls import url
from views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^login/$', login_view, name='login_view'),
	url(r'^home/$', home_page, name='home_page'),
	url(r'^logout/$', logout_view, name='logout_view'),
    # url(r'^projectbackend/', admin.site.urls),
    url(r'^register/$', register_view, name='register'),
    url(r'^add_books/$', add_books, name='add_books'),
    url(r'^add_publications/$', add_publications, name='add_publications'),
    url(r'^add_authors/$', add_authors, name='add_authors'),
    url(r'^add_genres/$', add_genres, name='add_genres'),
    url(r'^registeradmin/$', register_admin_view, name='register_admin_view'),
    url(r'^prefgenres/$', preferred_genres, name='preferred_genres'),
    url(r'^search/$', advanced_search, name='advanced_search'),
    url(r'^book/(?P<ISBN>[a-zA-Z0-9\-]+)$', book_details, name='book_details'),

    url(r'^api/update_rating$', update_rating_api, name='update_rating_api'),
    url(r'^api/update_review$', update_review_api, name='update_review_api'),
    url(r'^api/update_location$', update_location_api, name='update_location_api'),
    url(r'^api/update_review_helpful$', update_review_helpful_api, name='update_review_helpful_api'),

    url(r'^$', main_login_page, name='main_login_page'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)