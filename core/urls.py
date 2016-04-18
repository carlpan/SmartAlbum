from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^account/login/$', views.user_login, name='login'),
    url(r'^account/logout/$', views.user_logout, name='logout'),
]