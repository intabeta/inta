from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, Graph
from taggit.models import Tag
from math import sin, cos, pi
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates universe view'
    def handle(self, *args, **options):
        tags = Tag.objects.all()
        entries = Entry.objects.all()
        tagscores = dict()
        for method in ('votes','decay1','decay2','decay3','decay4','decay5','decay6','decay7','decay8'):
            edges=[]
            for tag in tags:
                tagscores[tag.id] = 0
            for entry in entries:
                etags = entry.tags.all()
                for i, tag1 in enumerate(etags):
                    rank1 = entry._get_ranking(tag1, method)
                    tagscores[tag1.id] += rank1
                    for tag2 in etags[i+1:]:
                        edges.append([tag1.id,tag2.id,int(round(rank1+entry._get_ranking(tag2,method)))])

            nztags = [ tag.id for tag in tags if round(tagscores[tag.id]) != 0 ] #nonzero tags
            edges2=[]
            for e in edges:
                if e[0] in nztags and e[1] in nztags and e[2]>0: #only consider edges that were connected to two nonzero tags and have nonzero strength
                    edges2.append(e)
            
            n = len(nztags)
            points= [ [nztags[i],int(round(tagscores[nztags[i]]))] for i in range(n) ]

            graph = Graph.objects.get(name = method)
            graph.points = points
            graph.edges = edges2
            graph.save()
            
