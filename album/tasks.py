import tweepy
from datetime import timedelta
from celery.task import task, periodic_task
from celery.schedules import crontab
from .views import show_photos

@periodic_task(run_every=timedelta(seconds=10))
def fetch_periodically_from_twitter():
    show_photos()
