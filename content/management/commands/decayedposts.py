from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os
from datetime import datetime, timedelta

class Command(BaseCommand):
    args = ''
    help = 'Decay for entry scores.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        for entry in entries:
            total = entry.posts + entry.double_posts * 2
            now = datetime.utcnow()
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            print lapsed.total_seconds()
            entry.decayed_score = total * (1 / 1.15 ** (lapsed.total_seconds() / 28800))
            print total, entry.decayed_score
            entry.save()
#             total = entry.posts + entry.double_posts * 2
#             if entry.last_score == 0:
#                 entry.last_score=1
#             entry.last_growth = ((total - entry.last_score)/entry.last_score) * 100
#             if entry.last_growth > 0.0:
#                 print entry, total, entry.last_growth
#             entry.last_score = total
#             entry.save()
#             
            
            
    

        self.stdout.write('Success\n')
