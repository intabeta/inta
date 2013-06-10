from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os
from datetime import datetime, timedelta

class Command(BaseCommand):
    args = ''
    help = 'Decay for entry scores.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        base = 0.5
        for entry in entries:
            now = datetime.utcnow()
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            entry.score = 0

            d1 = base ** (lapsed.total_seconds()/1800)
            d2 = base ** (lapsed.total_seconds()/10800)
            d3 = base ** (lapsed.total_seconds()/86400)
            d4 = base ** (lapsed.total_seconds()/259200)
            d5 = base ** (lapsed.total_seconds()/604800)
            d6 = base ** (lapsed.total_seconds()/2592000)
            d7 = base ** (lapsed.total_seconds()/7776000)
            d8 = base ** (lapsed.total_seconds()/31536000)

            entry.d1 = round(d1,4)
            entry.d2 = round(d2,4)
            entry.d3 = round(d3,4)
            entry.d4 = round(d4,4)
            entry.d5 = round(d5,4)
            entry.d6 = round(d6,4)
            entry.d7 = round(d7,4)
            entry.d8 = round(d8,4)
            
            for tag in entry.tags.all():
                total = entry._get_ranking(tag) #posts + 2*double_posts
                entry.score += total
                #print total
                #print(entry.title+'; '+tagnew.name)
            entry.save()
        self.stdout.write('Success\n')
