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

            d1 = base ** (lapsed.total_seconds()/1800)
            d2 = base ** (lapsed.total_seconds()/10800)
            d3 = base ** (lapsed.total_seconds()/86400)
            d4 = base ** (lapsed.total_seconds()/259200)
            d5 = base ** (lapsed.total_seconds()/604800)
            d6 = base ** (lapsed.total_seconds()/2592000)
            d7 = base ** (lapsed.total_seconds()/7776000)
            d8 = base ** (lapsed.total_seconds()/31536000)

            entry.decay_scalars = [d1,d2,d3,d4,d5,d6,d7,d8]
            
            for tagnew in entry.tags.all():
                total = entry._get_ranking(tagnew) #posts + 2*double_posts
                entry.score += total
                tval1=entry.decayed_score_1.tagval_set.get(tag__iexact=tagnew.name)
                tval1.val = round(total * d1,5)
                entry.score_d1 += tval1.val
                tval1.save()
                tval2=entry.decayed_score_2.tagval_set.get(tag__iexact=tagnew.name)
                tval2.val = round(total * d2,5)
                entry.score_d2 += tval2.val
                tval2.save()
                tval3=entry.decayed_score_3.tagval_set.get(tag__iexact=tagnew.name)
                tval3.val = round(total * d3,5)
                entry.score_d3 += tval3.val
                tval3.save()
                tval4=entry.decayed_score_4.tagval_set.get(tag__iexact=tagnew.name)
                tval4.val = round(total * d4,5)
                entry.score_d4 += tval4.val
                tval4.save()
                tval5=entry.decayed_score_5.tagval_set.get(tag__iexact=tagnew.name)
                tval5.val = round(total * d5,5)
                entry.score_d5 += tval5.val
                tval5.save()
                tval6=entry.decayed_score_6.tagval_set.get(tag__iexact=tagnew.name)
                tval6.val = round(total * d6,5)
                entry.score_d6 += tval6.val
                tval6.save()
                tval7=entry.decayed_score_7.tagval_set.get(tag__iexact=tagnew.name)
                tval7.val = round(total * d7,5)
                entry.score_d7 += tval7.val
                tval7.save()
                tval8=entry.decayed_score_8.tagval_set.get(tag__iexact=tagnew.name)
                tval8.val = round(total * d8,5)
                entry.score_d8 += tval8.val
                tval8.save()
                #print total
                #print(entry.title+'; '+tagnew.name)
            entry.save()
        self.stdout.write('Success\n')
