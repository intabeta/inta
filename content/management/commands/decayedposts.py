<<<<<<< HEAD
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
            base = 0.5
            entry.decayed_score_1 = total * (base ** (lapsed.total_seconds() / 1800)) #30 min
            entry.decayed_score_2 = total * (base ** (lapsed.total_seconds() / 10800)) #3 hours
            entry.decayed_score_3 = total * (base ** (lapsed.total_seconds() / 86400)) #1 day
            entry.decayed_score_4 = total * (base ** (lapsed.total_seconds() / 259200)) #3 days
            entry.decayed_score_5 = total * (base ** (lapsed.total_seconds() / 604800)) #1 week
            entry.decayed_score_6 = total * (base ** (lapsed.total_seconds() / 2592000)) #1 month (30 days)
            entry.decayed_score_7 = total * (base ** (lapsed.total_seconds() / 7776000)) #3 months
            entry.decayed_score_8 = total * (base ** (lapsed.total_seconds() / 31536000)) #1 year
            print total, entry.decayed_score_1
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
=======
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

            base = 0.5
            entry.decayed_score_1 = total * (base ** (lapsed.total_seconds() / 1800)) #30 min
            entry.decayed_score_2 = total * (base ** (lapsed.total_seconds() / 10800)) #3 hours
            entry.decayed_score_3 = total * (base ** (lapsed.total_seconds() / 86400)) #1 day
            entry.decayed_score_4 = total * (base ** (lapsed.total_seconds() / 259200)) #3 days
            entry.decayed_score_5 = total * (base ** (lapsed.total_seconds() / 604800)) #1 week
            entry.decayed_score_6 = total * (base ** (lapsed.total_seconds() / 2592000)) #1 month (30 days)
            entry.decayed_score_7 = total * (base ** (lapsed.total_seconds() / 7776000)) #3 months
            entry.decayed_score_8 = total * (base ** (lapsed.total_seconds() / 31536000)) #1 year

            print total, entry.decayed_score_1

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

>>>>>>> updated variable name
