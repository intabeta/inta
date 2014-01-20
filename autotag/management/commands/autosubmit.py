from django.core.management.base import BaseCommand, CommandError
from autotag.rss import submit_rss, urls
import os

class Command(BaseCommand):
    args = ''
    help = 'Autosubmits from rss'
    def handle(self, *args, **options):
        submit_rss(urls)
