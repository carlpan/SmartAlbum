from django.test import TestCase

from .models import Album, Image

# Create your tests here.

def create_album(name, capacity):
    return Album.objects.create(name=name, capacity=capacity)

def create_image(album, url, owner, likes):
    return Image.objects.create(album=album, image_url_name=url, owner=owner, total_likes=likes)

class AlbumViewTests(TestCase):
    def test_album_view_with_a_new_album(self):
        new_album = create_album(name='Nature', capacity=200)
        self.assertEqual(new_album.name, 'Nature')

    def test_album_view_with_a_new_image(self):
        new_album = create_album(name='Sun', capacity=100)
        url = 'http://pbs.twimg.com/media/Cba4UOpUsAAZ32J.jpg'
        new_image = create_image(new_album, url, 'Karl', 20)
        self.assertEqual(new_image.album.name, 'Sun')
        self.assertEqual(new_image.image_url_name, url)


