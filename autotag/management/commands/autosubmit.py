from django.core.management.base import BaseCommand, CommandError
from autotag.rss import rss_submit, urls
import os

class Command(BaseCommand):
    args = ''
    help = 'Autosubmits from rss'
    def handle(self, *args, **options):
        rss_submit(urls)
