from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^images/$', views.ImageListView.as_view(), name='image_list'),
    url(r'^images/(?P<pk>\d+)/$', views.ImageDetailView.as_view(), name='image_detail'),
]