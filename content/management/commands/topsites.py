from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top sites'
    def handle(self, *args, **options):
        topsitesdicts=[ Dict.objects.get(id=i) for i in range(1463,1472)]
        entries = Entry.objects.all()
        data = ((entry.domain,entry.score,entry.score*entry.d1,entry.score*entry.d2,entry.score*entry.d3,entry.score*entry.d4,entry.score*entry.d5,entry.score*entry.d6,entry.score*entry.d7,entry.score*entry.d8) for entry in entries)
        scores = dict()
        for datum in data:
            if not scores.__contains__(datum[0]):
                scores[datum[0]]=[0,0,0,0,0,0,0,0,0]
            for i in range(9):
                scores[datum[0]][i] += datum[i+1]
                
        for i, topsites in enumerate(topsitesdicts):
            topdomains = sorted(scores, key=lambda d: -scores[d][i])[:10]
            for tv in topsites.tagval_set.all():
                tv.delete()
            for td in topdomains:
                topsites.tagval_set.create(tag=td,val=scores[td][i])
                
        
