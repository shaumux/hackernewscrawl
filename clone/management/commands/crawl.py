import requests
import re
import logging
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from ...utils import save_updates

CRAWL_PAGE_COUNT = 3

TIME_UNITS = {
    ('second', 'seconds'): 'seconds',
    ('minute', 'minutes'): 'minutes',
    ('hour', 'hours'): 'hours',
    ('day', 'days'): 'days',
    ('week', 'weeks'): 'weeks'
}

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        articles = []
        for page in self.get_page():
            for article in self.get_article(page):
                try:
                    articles.append(self.get_article_props(article))
                except IndexError as exc:
                    logger.log(level=logging.ERROR, msg='{0}'.format(exc))
        save_updates(articles)

    def get_page(self):
        for count in xrange(CRAWL_PAGE_COUNT, 0, -1):
            yield requests.get('https://news.ycombinator.com/news?p={0}'.format(count)).content

    def get_article(self, content):
        soup = BeautifulSoup(content, 'lxml')
        tags = soup('tr', class_='athing')
        tags.reverse()
        for tag in tags:
            yield tag

    def get_article_props(self, article):
        url_tag = article('span', class_='deadmark').pop().next_sibling
        url = url_tag['href']

        title_text = url_tag.string

        prop_container = article.find_next_sibling()
        props = prop_container('td', class_='subtext').pop()

        post_time_string = props('a', href=re.compile('item\?id=\d+'),
                                 string=re.compile('\d+?\s+?\w+?\s+?ago')).pop().string
        post_time_diff = post_time_string.split(' ')
        post_time = self.calculate_time(int(post_time_diff[0]), post_time_diff[1])

        upvotes_string = props('span', class_='score').pop().string
        upvotes_count = int(upvotes_string.split(' ')[0])
        try:
            comment_tag = props('a', string=re.compile('\d+\s+comment')).pop()
        except IndexError as exc:
            comment_tag = props('a', string=re.compile('discuss')).pop()
            comment_count = 0
        else:
            comment_string = comment_tag.string
            comment_count = int(comment_string.split(' ')[0])

        hacker_news_url = 'http://news.ycombinator.com/{0}'.format(comment_tag['href'])

        return {
            'url': url,
            'hacker_news_url': hacker_news_url,
            'posted_on': post_time,
            'upvotes': upvotes_count,
            'comments': comment_count,
            'title': title_text
        }

    def calculate_time(self, magnitude, unit):
        key_find = lambda x: [k for k in TIME_UNITS if x in k]
        time_key = key_find(unit)[0]
        time_unit = TIME_UNITS[time_key]
        return datetime.now()-timedelta(**{time_unit: magnitude})
