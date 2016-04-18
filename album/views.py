from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from .models import Album, Image
from SmartAlbum.secrets import SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET
import tweepy
import facebook
import requests


# Create your views here.

@login_required
def album(request):
    # Get all images stored
    images = Image.objects.all()
    return render(request, 'album/album.html', {'images': images})


@login_required
def popular_photos(request):
    popular_images = Image.objects.order_by('total_likes')[:7].reverse()
    return render(request, 'album/popular_photos.html', {'popular_images': popular_images})


@login_required
def post_to_facebook(request):
    # Get app access token
    access_token = get_facebook_access_token(SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET)
    # Initialize graph api object
    graph = facebook.GraphAPI(access_token=access_token)
    attachment = {
        'name': 'Most popular photos from my Smart Album',
        'link': 'http://myalbumsite.com:8000/album/popular/'
    }
    graph.put_wall_post(message="Check this album out", attachment=attachment)

    return redirect(reverse('album:album'))


##############################
# Fetch photos from Twitter  #
##############################
def fetch_tweets_with_hashtag(hashtag):
    # Twitter keys
    consumer_key = '66hfo53Na6YGs2bf1w33Pjutb'
    consumer_secret_key = '9Nq3yRYhVHRnfVYVFGhg4cqluYEzAIFVUCIz29m3ZtgmE48GmT'
    access_token = '1403881585-PZZGHv6BMeCxKKtVdXhgR57L5t4G1WXLd86EJWU'
    access_token_secret = 'cn7TbbIdTt6myoocjz1iDZdV66lssivscXTWIErvXrKva'

    # Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search, q=hashtag).items(100)

    return tweets


def save_images_from_tweets(tweets):
    # lists to store results
    image_list = set()  # don't copy duplicate url strings
    owner_list = []
    likes_list = []

    # Create album
    album, created = Album.objects.get_or_create(name='My Hashtag Album')

    # Refer to Twitter API Overview for json structure
    for result in tweets:
        media = result.entities.get('media', [])
        if len(media) > 0:
            print media[0]['media_url']
            image_list.add(media[0]['media_url'])
            owner_list.append(result.user.name)
            # seems like favorite_count (likes) always give 0
            # use retweet_count instead for recording popularity
            likes_list.append(result.retweet_count)

    # Save the data to database
    index = 0
    for image in image_list:
        # make sure retrieving uniqe image url strings
        if not Image.objects.filter(image_url_name=image).exists():
            image = Image(image_url_name=image, owner=owner_list[index], total_likes=likes_list[index])
            image.album = album
            image.save()
        index += 1


#################
# Sending email #
#################
def send_mail_when_photo_capacity_reached():
    album = Album.objects.all()[0]
    album_capacity = album.capacity
    image_count = Image.objects.all().count()
    print image_count

    # Check image count, stop when album capacity (501 default) reached
    if image_count != 0:
        if image_count % 100 == 0 and image_count <= album_capacity:
            print "sent"
            subject = '#carnival has {} photos'.format(image_count)
            body = "I'm awesome"
            email = EmailMessage(subject, body, from_email='Hashtag@EversnapApp.com', to=['carlpan66@gmail.com'],
                                 bcc=['davide@geteversnap.com'])
            email.send()


###################
# Private methods #
###################
# Called in periodic task
def show_photos():
    carnival_tweets = fetch_tweets_with_hashtag('#carnival')
    save_images_from_tweets(carnival_tweets)
    send_mail_when_photo_capacity_reached()


# Get Facebook app access token
def get_facebook_access_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    result = file.text.split("=")[1]
    return result
