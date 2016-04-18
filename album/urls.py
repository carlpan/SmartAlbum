from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.album, name='album'),
    url(r'^popular/$', views.popular_photos, name='popular'),
    url(r'^post/$', views.post_to_facebook, name='post'),
]