from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    hacker_news_url = models.URLField(max_length=255, unique=True)
    posted_on = models.DateTimeField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    user_deleted = models.ManyToManyField(User, related_name='deleted_items')
    user_read = models.ManyToManyField(User, related_name='read_items')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
