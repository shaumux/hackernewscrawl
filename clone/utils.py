from .models import *
from django.db import transaction


@transaction.atomic
def save_updates(news_items=None):
    for news in news_items:
        NewsItem.objects.update_or_create(hacker_news_url=news['hacker_news_url'], defaults=news)
