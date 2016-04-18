from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.IntegerField(default=501)

    def __str__(self):
        return self.name

class Image(models.Model):
    album = models.ForeignKey(Album, related_name='images', blank=False)
    image_url_name = models.CharField(max_length=300)
    store_date = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=200)
    total_likes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.image_url_name
