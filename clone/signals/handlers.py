from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.core.management import call_command

@receiver(user_logged_in)
def my_handler(sender, **kwargs):
    call_command('crawl')