from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, DataList
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

        domains = scores.keys()
        for domain in domains:
            for i, method in enumerate(('votes','decay1','decay2','decay3','decay4','decay5','decay6','decay7','decay8')):
                posts = sorted([ [e.id, entry.score * (1,entry.d1,entry.d2,entry.d3,entry.d4,entry.d5,entry.d6,entry.d7,entry.d8)[i]] for e in Entry.objects.filter(domain=domain) ], key=lambda a: -a[1])
                postsdatalist, c = DataList.objects.get_or_create(name='top_'+method+'_site:'+domain)
                postsdatalist.data = [ p[0] for p in posts ]
                postsdatalist.save()
                
                
        
