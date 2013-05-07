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
            now = datetime.utcnow()
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            for tagnew in entry.tags.all():
                total = entry._get_ranking(tagnew) #posts + 2*double_posts
                print lapsed.total_seconds()
                base = 0.5
                tval1=entry.decayed_score_1.tagval_set.get(tag=tagnew)
                tval1.val = total * (base ** (lapsed.total_seconds() / 1800))
                tval1.save()
                tval2=entry.decayed_score_2.tagval_set.get(tag=tagnew)
                tval2.val = total * (base ** (lapsed.total_seconds() / 10800))
                tval2.save()
                tval3=entry.decayed_score_3.tagval_set.get(tag=tagnew)
                tval3.val = total * (base ** (lapsed.total_seconds() / 86400))
                tval3.save()
                tval4=entry.decayed_score_4.tagval_set.get(tag=tagnew)
                tval4.val = total * (base ** (lapsed.total_seconds() / 259200))
                tval4.save()
                tval5=entry.decayed_score_5.tagval_set.get(tag=tagnew)
                tval5.val = total * (base ** (lapsed.total_seconds() / 604800))
                tval5.save()
                tval6=entry.decayed_score_6.tagval_set.get(tag=tagnew)
                tval6.val = total * (base ** (lapsed.total_seconds() / 2592000))
                tval6.save()
                tval7=entry.decayed_score_7.tagval_set.get(tag=tagnew)
                tval7.val = total * (base ** (lapsed.total_seconds() / 7776000))
                tval7.save()
                tval8=entry.decayed_score_8.tagval_set.get(tag=tagnew)
                tval8.val = total * (base ** (lapsed.total_seconds() / 31536000))
                tval8.save()
                #print total
                #print(entry.title+'; '+tagnew.name)
        self.stdout.write('Success\n')
