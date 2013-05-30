from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, DataList
from taggit.models import Tag
from math import sin, cos, pi, ceil
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates universe view'
    def handle(self, *args, **options):
        tags = Tag.objects.all()
        tagnames = [ str(t.name) for t in tags ]
        entries = Entry.objects.all()
        tagscores = dict()
        for method, datalist in zip(['votes','decay1','decay2','decay3','decay4','decay5','decay6','decay7','decay8'],[ DataList.objects.get(id=i) for i in range(3000,3009) ]):
            edges=[]
            for tag in tagnames:
                tagscores[tag] = 0
            for entry in entries:
                etags = entry.tags.all()
                for i, tag1 in enumerate(etags):
                    rank1 = entry._get_ranking(tag1, method)
                    tagscores[tag1.name] += rank1
                    for tag2 in etags[i+1:]:
                        edges.append([tag1.name,tag2.name,ceil(rank1+entry._get_ranking(tag2,method))])

            nztags = [ tag for tag in tagnames if round(tagscores[tag]) != 0 ] #nonzero tags
            edges2=[]
            for e in edges:
                if e[0] in nztags and e[1] in nztags: #only consider edges that were connected to two nonzero tags
                    edges2.append([nztags.index(e[0]),nztags.index(e[1]),e[2]])
            
            n = len(nztags)
            points= [ [200+100*cos(2*pi*i/n),200+100*sin(2*pi*i/n),nztags[i],round(tagscores[nztags[i]])] for i in range(n) ]

            datalist.data = [points,edges2]
            datalist.save()
            
