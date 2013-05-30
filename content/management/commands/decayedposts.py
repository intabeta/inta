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
            entry.score_d1 = 0
            entry.score_d2 = 0
            entry.score_d3 = 0
            entry.score_d4 = 0
            entry.score_d5 = 0
            entry.score_d6 = 0
            entry.score_d7 = 0
            entry.score_d8 = 0
            for tagnew in entry.tags.all():
                total = entry._get_ranking(tagnew) #posts + 2*double_posts
                entry.score += total
                tval1=entry.decayed_score_1.tagval_set.get(tag__iexact=tagnew)
                tval1.val = round(total * (base ** (lapsed.total_seconds() / 1800)),5)
                entry.score_d1 += tval1.val
                tval1.save()
                tval2=entry.decayed_score_2.tagval_set.get(tag__iexact=tagnew)
                tval2.val = round(total * (base ** (lapsed.total_seconds() / 10800)),5)
                entry.score_d2 += tval2.val
                tval2.save()
                tval3=entry.decayed_score_3.tagval_set.get(tag__iexact=tagnew)
                tval3.val = round(total * (base ** (lapsed.total_seconds() / 86400)),5)
                entry.score_d3 += tval3.val
                tval3.save()
                tval4=entry.decayed_score_4.tagval_set.get(tag__iexact=tagnew)
                tval4.val = round(total * (base ** (lapsed.total_seconds() / 259200)),5)
                entry.score_d4 += tval4.val
                tval4.save()
                tval5=entry.decayed_score_5.tagval_set.get(tag__iexact=tagnew)
                tval5.val = round(total * (base ** (lapsed.total_seconds() / 604800)),5)
                entry.score_d5 += tval5.val
                tval5.save()
                tval6=entry.decayed_score_6.tagval_set.get(tag__iexact=tagnew)
                tval6.val = round(total * (base ** (lapsed.total_seconds() / 2592000)),5)
                entry.score_d6 += tval6.val
                tval6.save()
                tval7=entry.decayed_score_7.tagval_set.get(tag__iexact=tagnew)
                tval7.val = round(total * (base ** (lapsed.total_seconds() / 7776000)),5)
                entry.score_d7 += tval7.val
                tval7.save()
                tval8=entry.decayed_score_8.tagval_set.get(tag__iexact=tagnew)
                tval8.val = round(total * (base ** (lapsed.total_seconds() / 31536000)),5)
                entry.score_d8 += tval8.val
                tval8.save()
                #print total
                #print(entry.title+'; '+tagnew.name)
            entry.save()
        self.stdout.write('Success\n')
